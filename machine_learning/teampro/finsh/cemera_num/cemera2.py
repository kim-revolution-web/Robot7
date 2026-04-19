from __future__ import annotations

import base64
import json
import os
import threading
import time
from dataclasses import dataclass
from queue import Empty, Queue
from typing import Optional, Tuple

import cv2
import numpy as np

# TensorFlow (shape model)
import tensorflow as tf

# pip install websocket-client
try:
    import websocket  # type: ignore
except Exception:
    websocket = None


@dataclass
class LineResult:
    found: bool
    error_px: float = 0.0          # 가운데 기준: 왼쪽(+) / 오른쪽(-)
    white_ratio: float = 0.0       # 0~1
    white_pixels: int = 0


@dataclass
class ShapeResult:
    found: bool
    name: str = "NONE"
    confidence: float = 0.0        # 0~100
    white_ratio_pct: float = 0.0   # 0~100


class RosbridgeCompressedImageReceiver:
    """
    rosbridge_websocket으로 sensor_msgs/CompressedImage 토픽을 subscribe해서
    JPEG(base64)를 cv2 프레임(BGR)로 바꿔 최신 프레임만 제공.
    """
    def __init__(
        self,
        ws_url: str,
        image_topic: str,
        throttle_rate_ms: int = 80,
        queue_size: int = 1,
        connect_timeout: float = 5.0,
    ):
        if websocket is None:
            raise RuntimeError(
                "websocket-client가 설치되어 있지 않습니다. "
                "노트북에서 실행한다면: pip install websocket-client"
            )

        self.ws_url = ws_url
        self.image_topic = image_topic
        self.throttle_rate_ms = int(throttle_rate_ms)

        self._running = True
        self._q: Queue[np.ndarray] = Queue(maxsize=max(1, int(queue_size)))

        self.ws = websocket.WebSocket()
        self.ws.settimeout(connect_timeout)
        self.ws.connect(self.ws_url)

        sub_msg = {
            "op": "subscribe",
            "topic": self.image_topic,
            "type": "sensor_msgs/CompressedImage",
            "throttle_rate": self.throttle_rate_ms,  # ms
            "queue_length": 1,
        }
        self.ws.send(json.dumps(sub_msg))

        self._th = threading.Thread(target=self._recv_loop, daemon=True)
        self._th.start()

    def _recv_loop(self):
        while self._running:
            try:
                raw = self.ws.recv()
                if not raw:
                    continue
                data = json.loads(raw)
                msg = data.get("msg")
                if not msg:
                    continue
                b64 = msg.get("data")
                if not b64:
                    continue

                jpg_bytes = base64.b64decode(b64)
                arr = np.frombuffer(jpg_bytes, dtype=np.uint8)
                frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
                if frame is None:
                    continue

                # keep only newest
                while True:
                    try:
                        self._q.get_nowait()
                    except Empty:
                        break
                try:
                    self._q.put_nowait(frame)
                except Exception:
                    pass

            except Exception:
                time.sleep(0.1)

    def read(self, timeout: float = 0.8) -> Tuple[bool, Optional[np.ndarray]]:
        try:
            frame = self._q.get(timeout=timeout)
            return True, frame
        except Empty:
            return False, None

    def close(self):
        self._running = False
        try:
            try:
                unsub_msg = {"op": "unsubscribe", "topic": self.image_topic}
                self.ws.send(json.dumps(unsub_msg))
            except Exception:
                pass
            self.ws.close()
        except Exception:
            pass


class CameraSystem:
    """
    ✅ 요구사항 반영:
    - 로봇 카메라(rosbridge compressed) 사용
    - flip 제거
    - AUTO에서만 라인트레이싱/도형인식 가동 (MANUAL은 완전 idle)
    - AUTO에서만 line lost -> AUTO_STOP 전송 (MANUAL에서는 절대 STOP/라인명령 보내지 않음)
    - 도형인식: TensorFlow 모델(shape_model_6.keras) 기반 (모델명 변경 X)
    - shape ROI(상단) 좌표를 기준으로:
      - 라인트레이싱 ROI를 "shape 사각형 아래"에, 같은 가로 범위로 맞춤
      - width의 1/2 영역만 사용 (shape.py에서 쓰던 x1/x2 그대로 사용)
    - show=True/False로 imshow on/off
    """

    def __init__(
        self,
        robot,
        show: bool = True,
        show_line_binary: bool = False,  # 라인트레이싱 이진화 화면 표시
        width: int = 640,
        height: int = 480,
        # --- 로봇 카메라(ROS compressed) ---
        ws_url: str = "ws://192.168.0.93:9090",
        image_topic: str = "/camera/image_raw/compressed",
        throttle_rate_ms: int = 80,
        # --- 라인트레이싱 설정 ---
        fixed_thresh_val: int = 120,
        full_threshold: float = 0.80,
        deadzone_px: int = 20,
        # --- Shape(딥러닝) 설정 ---
        model_path: str = "shape_model_6.keras",
        img_size: int = 128,
        shape_ratio_min: float = 5.0,    # %
        shape_ratio_max: float = 17.0,   # %
        shape_conf_th: float = 95.0,     # %
        shape_action_cooldown_sec: float = 2.0,  # 도형 행동 트리거 쿨다운
        # --- ROI (shape.py 좌표 기반: 640x480 기준) ---
        shape_x1: int = 180,
        shape_x2: int = 480,
        shape_y1: int = 0,
        shape_y2: int = 320,
    ):
        self.robot = robot
        self.show = bool(show)
        self.show_line_binary = bool(show_line_binary)

        self.width = int(width)
        self.height = int(height)
        self.target_center = self.width // 2  # 전체 프레임 중앙(왼+ / 오- 기준)

        # ROS 이미지
        self.ws_url = str(ws_url)
        self.image_topic = str(image_topic)
        self.throttle_rate_ms = int(throttle_rate_ms)

        # Line config
        self.fixed_thresh_val = int(fixed_thresh_val)
        self.full_threshold = float(full_threshold)
        self.deadzone_px = int(deadzone_px)

        # Shape model
        self.model_path = str(model_path)
        self.img_size = int(img_size)
        self.shape_ratio_min = float(shape_ratio_min)
        self.shape_ratio_max = float(shape_ratio_max)
        self.shape_conf_th = float(shape_conf_th)
        self.shape_action_cooldown_sec = float(shape_action_cooldown_sec)
        self._last_shape_action_time = 0.0
        self.class_names = ["circle", "rectangle", "triangle", "x"]

        self.model = None
        if os.path.exists(self.model_path):
            try:
                self.model = tf.keras.models.load_model(self.model_path)
            except Exception as e:
                print(f"[camera] ERROR: 모델 로드 실패: {e}")
                self.model = None
        else:
            print(f"[camera] WARN: 모델 파일 없음: {self.model_path}")

        # ROI: shape 영역(상단) + line 영역(하단, shape 아래)
        self.shape_x1 = int(shape_x1)
        self.shape_x2 = int(shape_x2)
        self.shape_y1 = int(shape_y1)
        self.shape_y2 = int(shape_y2)

        # line ROI는 shape 사각형 아래, 같은 x 범위, 아래쪽 끝까지
        self.line_x1 = self.shape_x1
        self.line_x2 = self.shape_x2
        self.line_y1 = self.shape_y2
        self.line_y2 = self.height

                # last debug images
        self._last_line_thr: Optional[np.ndarray] = None

# status text
        self.line_status = "IDLE"
        self.shape_status = "IDLE"

        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False

    # -----------------------------
    # 라인트레이싱: line ROI에서만 계산
    # -----------------------------
    def _detect_line(self, frame_bgr: np.ndarray) -> LineResult:
        img = frame_bgr
        h, w = img.shape[:2]

        x1 = int(np.clip(self.line_x1, 0, w - 1))
        x2 = int(np.clip(self.line_x2, x1 + 1, w))
        y1 = int(np.clip(self.line_y1, 0, h - 1))
        y2 = int(np.clip(self.line_y2, y1 + 1, h))

        roi = img[y1:y2, x1:x2]

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)

        # 고정 임계값 + 흑선 가정(반전)
        _, thr = cv2.threshold(blurred, self.fixed_thresh_val, 255, cv2.THRESH_BINARY_INV)
        self._last_line_thr = thr

        white_pixels = int(cv2.countNonZero(thr))
        total_pixels = int(thr.shape[0] * thr.shape[1])
        white_ratio = (white_pixels / total_pixels) if total_pixels > 0 else 0.0

        # 너무 꽉 차면(바닥/그림자) -> line lost로 간주
        if white_ratio > self.full_threshold or white_pixels == 0:
            return LineResult(found=False, error_px=0.0, white_ratio=white_ratio, white_pixels=white_pixels)

        M = cv2.moments(thr)
        if M["m00"] <= 0:
            return LineResult(found=False, error_px=0.0, white_ratio=white_ratio, white_pixels=white_pixels)

        cx_roi = float(M["m10"] / M["m00"])   # roi 기준
        cx_global = cx_roi + x1               # 프레임 기준 x
        error_px = float(self.target_center - cx_global)  # ✅ 왼쪽(+) / 오른쪽(-)

        return LineResult(found=True, error_px=error_px, white_ratio=white_ratio, white_pixels=white_pixels)

    # -----------------------------
    # 도형인식: shape ROI에서 TF 모델로 예측
    # -----------------------------
    def _detect_shape_tf(self, frame_bgr: np.ndarray) -> ShapeResult:
        if self.model is None:
            return ShapeResult(found=False, name="NONE", confidence=0.0, white_ratio_pct=0.0)

        img = frame_bgr
        h, w = img.shape[:2]

        x1 = int(np.clip(self.shape_x1, 0, w - 1))
        x2 = int(np.clip(self.shape_x2, x1 + 1, w))
        y1 = int(np.clip(self.shape_y1, 0, h - 1))
        y2 = int(np.clip(self.shape_y2, y1 + 1, h))

        roi = img[y1:y2, x1:x2]

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        margin = 5
        if thresh.shape[0] > margin * 2 and thresh.shape[1] > margin * 2:
            thresh = thresh[margin:-margin, margin:-margin]

        resized = cv2.resize(thresh, (self.img_size, self.img_size))

        total_pixels = resized.size
        white_pixels = int(np.sum(resized == 255))
        white_ratio_pct = (white_pixels / total_pixels) * 100.0 if total_pixels > 0 else 0.0

        # shape.py 규칙 유지: ratio 구간일 때만 모델 추론
        if not (self.shape_ratio_min <= white_ratio_pct < self.shape_ratio_max):
            return ShapeResult(found=False, name="NONE", confidence=0.0, white_ratio_pct=white_ratio_pct)

        input_data = resized.reshape(1, self.img_size, self.img_size, 1).astype("float32")
        pred = self.model.predict(input_data, verbose=0)
        idx = int(np.argmax(pred))
        conf = float(np.max(pred) * 100.0)
        name = self.class_names[idx]

        found = conf >= self.shape_conf_th
        return ShapeResult(found=found, name=name if found else "NONE", confidence=conf, white_ratio_pct=white_ratio_pct)

    # -----------------------------
    # 입력 소스 열기
    # -----------------------------
    def _open_source(self):
        rx = RosbridgeCompressedImageReceiver(
            ws_url=self.ws_url,
            image_topic=self.image_topic,
            throttle_rate_ms=self.throttle_rate_ms,
            queue_size=1,
        )

        def read_fn():
            return rx.read(timeout=0.8)

        def close_fn():
            rx.close()

        print(f"[camera] Using ROS image via rosbridge: {self.ws_url} topic={self.image_topic}")
        return read_fn, close_fn

    # -----------------------------
    # 메인 루프
    # -----------------------------
    def _loop(self):
        try:
            read_frame, close_source = self._open_source()
        except Exception as e:
            print(f"[camera] ERROR: {e}")
            self._running = False
            return

        if self.show:
            cv2.namedWindow("Main View", cv2.WINDOW_NORMAL)

        # 부담 줄이기: TF 추론은 매 프레임 말고 N프레임마다
        shape_every = 3
        shape_counter = 0

        try:
            while self._running and getattr(self.robot, "is_running", True):
                ret, frame = read_frame()
                if not ret or frame is None:
                    continue

                # ✅ flip 없음
                img = cv2.resize(frame, (self.width, self.height))
                mode = getattr(self.robot, "control_mode", "MANUAL")

                line_res = LineResult(found=False)
                shape_res = ShapeResult(found=False)

                if mode == "AUTO":
                    # line: 매 프레임
                    line_res = self._detect_line(img)

                    # shape: 주기적으로
                    if shape_counter % shape_every == 0:
                        shape_res = self._detect_shape_tf(img)
                        try:
                            setattr(self.robot, "current_shape", shape_res.name if shape_res.found else "NONE")
                        except Exception:
                            pass
                    shape_counter += 1

                    # AUTO에서만 명령 전송
                    if not line_res.found:
                        self.line_status = "LINE LOST -> STOP"
                        if getattr(self.robot, "command_queue", None) is not None:
                            self.robot.command_queue.put({"source": "CAMERA", "cmd": "AUTO_STOP"})
                    else:
                        if abs(line_res.error_px) <= self.deadzone_px:
                            self.line_status = f"LINE OK (err={line_res.error_px:.1f}px)"
                        else:
                            self.line_status = f"LINE TRACK (err={line_res.error_px:.1f}px)"

                        if getattr(self.robot, "command_queue", None) is not None:
                            self.robot.command_queue.put({
                                "source": "CAMERA",
                                "cmd": "AUTO_LINE",
                                "value": float(line_res.error_px),
                            })

                    # shape status
                    if shape_res.found:
                        self.shape_status = f"SHAPE: {shape_res.name} ({shape_res.confidence:.1f}%)"
                    else:
                        self.shape_status = f"SHAPE: NONE (ratio={shape_res.white_ratio_pct:.1f}%)"

                    # ✅ 도형 행동 트리거(로봇이 처리)
                    if shape_res.found and getattr(self.robot, "command_queue", None) is not None:
                        now = time.time()
                        if (now - self._last_shape_action_time) >= self.shape_action_cooldown_sec:
                            self._last_shape_action_time = now
                            self.robot.command_queue.put({
                                "source": "CAMERA",
                                "cmd": "SHAPE_ACTION",
                                "name": str(shape_res.name).upper(),
                                "confidence": float(shape_res.confidence),
                            })

                else:
                    # MANUAL: 부담 줄이기 위해 아무것도 안 함
                    self.line_status = "MANUAL (line idle)"
                    self.shape_status = "MANUAL (shape idle)"
                    shape_counter = 0
                    try:
                        setattr(self.robot, "current_shape", "NONE")
                    except Exception:
                        pass

                # ----------------- 화면 표시 -----------------
                if self.show:
                    overlay = img.copy()

                    # ROI 표시
                    # shape ROI (상단)
                    cv2.rectangle(overlay, (self.shape_x1, self.shape_y1), (self.shape_x2, self.shape_y2), (255, 0, 0), 2)
                    cv2.putText(overlay, "SHAPE ROI", (self.shape_x1 + 5, self.shape_y1 + 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 0, 0), 2)

                    # line ROI (하단, shape 아래, 같은 x범위)
                    cv2.rectangle(overlay, (self.line_x1, self.line_y1), (self.line_x2, self.line_y2), (0, 255, 255), 2)
                    cv2.putText(overlay, "LINE ROI", (self.line_x1 + 5, self.line_y1 + 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)

                    # 중앙 기준선(전체 프레임 기준)
                    cv2.line(overlay, (self.target_center, 0), (self.target_center, self.height - 1), (0, 255, 0), 2)

                    # 텍스트
                    lin = float(getattr(self.robot, "current_lin_vel", 0.0))
                    ang = float(getattr(self.robot, "current_ang_vel", 0.0))
                    cv2.putText(overlay, f"MODE: {mode}", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                    cv2.putText(overlay, f"VEL: lin={lin:.3f}  ang={ang:.3f}", (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    cv2.putText(overlay, f"LINE: {self.line_status}", (10, 90),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
                    cv2.putText(overlay, f"{self.shape_status}", (10, 120),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
                    cv2.putText(overlay, f"SHAPE_STATE: {getattr(self.robot, 'current_shape', 'NONE')}", (10, 150),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

                    # 라인트레이싱 이진화(임시 디버그)
                    if self.show_line_binary and self._last_line_thr is not None:
                        thr_vis = cv2.resize(self._last_line_thr, (self.line_x2 - self.line_x1, self.line_y2 - self.line_y1))
                        cv2.imshow("Line Threshold", thr_vis)
                    cv2.imshow("Main View", overlay)
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord("q"):
                        setattr(self.robot, "is_running", False)
                        self._running = False
                        break

        finally:
            try:
                close_source()
            except Exception:
                pass
            if self.show:
                try:
                    cv2.destroyAllWindows()
                except Exception:
                    pass
