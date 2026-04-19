import cv2
import numpy as np
import threading
import time
from queue import Queue

class RobotSystem:
    def __init__(self):
        self.is_running = True
        self.control_mode = "AUTO"
        self.command_queue = Queue()

        # --- 라인추종 튜닝 값 ---
        self.target_center = 320          # 화면 중앙 목표 x좌표
        self.deadzone = 20                # 중앙 근처 허용 오차
        self.full_threshold = 0.8         # ROI가 너무 하얗게 꽉 차면 STOP(반사/과노출 방지)
        self.fixed_thresh_val = 120       # 고정 이진화 임계값

        # OpenCV 스레드 시작
        self.thread = threading.Thread(target=self.opencv_thread)
        self.thread.daemon = True
        self.thread.start()

    def opencv_thread(self):
        print(f"[AUTO] 시스템 시작 ")

        # 1) PC 웹캠 열기
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("에러: 캠을 찾을 수 없습니다.")
            return

        # 2) 디버그 창 생성(크기 조절 가능)
        cv2.namedWindow("Main View", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Check 1: ROI", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Check 2: Warped ROI", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Check 3: Binary View", cv2.WINDOW_NORMAL)

        while self.is_running:
            ret, frame = cap.read()
            if not ret:
                break

            # ---- 전처리: 좌우반전 + 리사이즈 ----
            img = cv2.flip(frame, 1)
            img = cv2.resize(img, (640, 480))
            h, w = img.shape[:2]

            if self.control_mode == "AUTO":
                # ============================================================
                # [PIPELINE 1] ROI(사각형)로 자르기
                #  - ROI = 네모(사각형) 영역으로 잘라내는 코드다.
                #  - 바닥 라인은 보통 아래쪽에 있으니 y를 320~480만 본다.
                #  - x는 중앙 근처만 보기 위해 center_x 기준으로 폭을 잡는다.
                # ============================================================
                y1, y2 = 320, 480      # ROI 세로 범위(아래쪽)
                roi_rate = 2
                roi_size = 80
                center_x = int(2 * w / 4)  # = w/2

                # ROI 좌표 계산(화면 밖으로 나가지 않게 clamp)
                x1 = max(0, int(center_x - roi_rate * roi_size))
                x2 = min(w, int(center_x + roi_rate * roi_size))

                roi_w, roi_h = x2 - x1, y2 - y1
                roi_raw = img[y1:y2, x1:x2].copy()   # ROI 네모로 잘라낸 이미지(컬러)

                # ============================================================
                # [PIPELINE 2] 원근 변환(사다리꼴 → 직사각형)
                #  - 바닥 라인은 원근 때문에 위로 갈수록 좁아 보임
                #  - src_pts(사다리꼴 4점) → dst_pts(직사각형 4점) 으로 펴준다
                # ============================================================
                top_ratio = 0.8
                top_width = roi_w * top_ratio
                top_margin = (roi_w - top_width) / 2

                # ROI 내부 좌표 기준 사다리꼴 4점
                src_pts = np.float32([
                    [top_margin, 0],                 # 좌상
                    [roi_w - top_margin, 0],         # 우상
                    [roi_w, roi_h],                  # 우하
                    [0, roi_h]                       # 좌하
                ])

                # 목표(직사각형) 4점
                dst_pts = np.float32([
                    [0, 0], [roi_w, 0], [roi_w, roi_h], [0, roi_h]
                ])

                matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
                roi_color = cv2.warpPerspective(roi_raw, matrix, (roi_w, roi_h))

                # ============================================================
                # [PIPELINE 3] 그레이/블러/이진화
                #  - 검은 선을 찾기 위해 THRESH_BINARY_INV 사용(선이 흰색이 됨)
                # ============================================================
                gray = cv2.cvtColor(roi_color, cv2.COLOR_BGR2GRAY)
                blurred = cv2.GaussianBlur(gray, (9, 9), 0)
                _, thresh = cv2.threshold(
                    blurred, self.fixed_thresh_val, 255, cv2.THRESH_BINARY_INV
                )

                # ============================================================
                # [PIPELINE 4] 흰 픽셀 비율 + 모멘트(무게중심)
                #  - white_ratio가 너무 크면(거의 전체가 흰색) 과검출 → STOP
                #  - moments로 라인 중심(cx)을 구함
                # ============================================================
                total_pixels = thresh.shape[0] * thresh.shape[1]
                white_pixels = cv2.countNonZero(thresh)
                white_ratio = white_pixels / total_pixels
                M = cv2.moments(thresh)

                # ============================================================
                # [PIPELINE 5] 판단 → 명령 생성(큐로 보냄)
                # ============================================================
                status_text = "LOST"
                display_color = (0, 0, 255)

                if white_ratio > self.full_threshold:
                    # ROI가 너무 하얗다 = 반사/과노출/노이즈 가능 → STOP
                    status_text, display_color = "STOP", (0, 0, 255)
                    self.command_queue.put({'source': 'CAMERA', 'cmd': 'STOP'})

                elif white_pixels == 0:
                    # 라인을 아예 못 찾음 → STOP
                    status_text, display_color = "LINE LOST! (STOP)", (0, 0, 255)
                    self.command_queue.put({'source': 'CAMERA', 'cmd': 'STOP'})

                elif M['m00'] > 0:
                    # 라인 중심(cx) 계산
                    cx_roi = int(M['m10'] / M['m00'])
                    cx_global = cx_roi + x1

                    # 중앙(목표) 대비 오차
                    error_value = self.target_center - cx_global

                    # 데드존이면 직진
                    if abs(error_value) <= self.deadzone:
                        status_text, display_color = "GO", (255, 255, 0)
                        self.command_queue.put({'source': 'CAMERA', 'cmd': 'AUTO_GO', 'value': error_value})

                    # 오차가 +면 LEFT 보정
                    elif error_value > 0:
                        status_text, display_color = f"LEFT: +{abs(round(error_value, 1))}", (0, 255, 0)
                        self.command_queue.put({'source': 'CAMERA', 'cmd': 'AUTO_LEFT', 'value': error_value})

                    # 오차가 -면 RIGHT 보정
                    else:
                        status_text, display_color = f"RIGHT: -{abs(round(error_value, 1))}", (0, 165, 255)
                        self.command_queue.put({'source': 'CAMERA', 'cmd': 'AUTO_RIGHT', 'value': error_value})

                    # 중심점 표시
                    cv2.circle(img, (cx_global, int(y1 + roi_h/2)), 10, (0, 0, 255), -1)

                else:
                    # 예외 상황
                    self.command_queue.put({'source': 'CAMERA', 'cmd': 'STOP'})

                # ============================================================
                # [PIPELINE 6] 시각화(디버그)
                # ============================================================

                # ROI 네모(사각형) 표시
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)

                # 원근 사다리꼴 표시(전체 화면 좌표로 변환)
                trap_pts = np.array([
                    [src_pts[0][0] + x1, src_pts[0][1] + y1],
                    [src_pts[1][0] + x1, src_pts[1][1] + y1],
                    [src_pts[2][0] + x1, src_pts[2][1] + y1],
                    [src_pts[3][0] + x1, src_pts[3][1] + y1]
                ], dtype=np.int32)
                cv2.polylines(img, [trap_pts], True, (0, 0, 255), 2)

                # 데드존 경계 표시
                left_boundary = self.target_center - self.deadzone
                right_boundary = self.target_center + self.deadzone
                cv2.line(img, (left_boundary, y1), (left_boundary, y2), (0, 255, 255), 2)
                cv2.line(img, (right_boundary, y1), (right_boundary, y2), (0, 255, 255), 2)

                cv2.putText(img, status_text, (10, 45),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, display_color, 3)

                # 디버그 창 출력
                cv2.imshow("Check 1: ROI", roi_raw)
                cv2.imshow("Check 2: Warped ROI", roi_color)
                cv2.imshow("Check 3: Binary View", thresh)

            # 메인 화면 출력
            cv2.imshow("Main View", img)

            # 키 입력
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                self.is_running = False
            elif key == ord('m'):
                self.control_mode = "MANUAL" if self.control_mode == "AUTO" else "AUTO"

        cap.release()
        cv2.destroyAllWindows()
