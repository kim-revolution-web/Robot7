import time
import threading
from queue import Queue

import cv2
import numpy as np

from link import RosbridgePublisher  # Rosbridge로 /cmd_vel publish, 카메라 subscribe 등을 해주는 클래스(네 코드 기준)


class RobotSystem:
    def __init__(self):
        # -------------------------------
        # 시스템 상태
        # -------------------------------
        self.is_running = True                  # 전체 루프/스레드 계속 돌릴지 여부
        self.control_mode = "MANUAL"            # "MANUAL" 또는 "AUTO"

        # -------------------------------
        # 명령 전달 큐
        #  - GUI / OpenCV 스레드가 여기로 명령(dict)을 넣음
        #  - main_controller가 여기서 꺼내서 처리함
        # -------------------------------
        self.command_queue = Queue()

        # -------------------------------
        # 현재 로봇 속도 상태 (최종 publish 되는 값)
        # -------------------------------
        self.current_lin_vel = 0.0              # 선속도 (전진/후진)
        self.current_ang_vel = 0.0              # 각속도 (좌/우 회전)

        # -------------------------------
        # 수동 조작 시 속도 변화량(누를 때마다 얼마나 바뀌는지)
        # -------------------------------
        self.lin_step = 0.005                   # 전진/후진 속도 증가/감소 단위
        self.ang_step = 0.02                    # 회전 속도 증가/감소 단위

        # -------------------------------
        # 속도 제한 (클램프)
        # -------------------------------
        self.MAX_LIN = 0.15                     # 선속도 최대값
        self.MAX_ANG = 1.0                      # 각속도 최대값

        # -------------------------------
        # 입력이 없을 때 “부드럽게 감속”하기 위한 감속 비율
        # -------------------------------
        self.lin_decel_rate = 0.002             # 선속도 감속률
        self.ang_decel_rate = 0.01              # 각속도 감속률

        # -------------------------------
        # [AUTO(자율주행/라인추종) 관련 설정]
        # -------------------------------
        self.auto_speed = 0.08                  # AUTO 모드에서 기본 전진 속도
        self.p_gain = 0.003                     # 라인 중심 오차(error)에 대한 P제어 게인(민감도)

        # -------------------------------
        # ROSBridge 통신 객체
        # -------------------------------
        self.publisher = RosbridgePublisher(
            ws_url="ws://192.168.0.68:9090"
        )

    # -------------------------------------------------------
    # 입력이 없을 때 속도를 “천천히 0으로” 당겨주는 함수들
    # -------------------------------------------------------
    def smooth_stop_linear(self):
        """선속도를 0으로 서서히 감속"""
        if self.current_lin_vel > 0:
            self.current_lin_vel = max(0.0, self.current_lin_vel - self.lin_decel_rate)
        elif self.current_lin_vel < 0:
            self.current_lin_vel = min(0.0, self.current_lin_vel + self.lin_decel_rate)

    def smooth_stop_angular(self):
        """각속도를 0으로 서서히 감속"""
        if self.current_ang_vel > 0:
            self.current_ang_vel = max(0.0, self.current_ang_vel - self.ang_decel_rate)
        elif self.current_ang_vel < 0:
            self.current_ang_vel = min(0.0, self.current_ang_vel + self.ang_decel_rate)

    # ---------------------------------
    # 메인 제어 루프 (핵심)
    #  - 큐에서 명령을 꺼내고
    #  - 모드(MANUAL/AUTO)와 source에 따라 속도 갱신
    #  - 최종적으로 /cmd_vel publish
    # ---------------------------------
    def main_controller(self):
        print("[RobotSystem] 제어 루프 시작")

        while self.is_running:
            # 1) 큐에 들어온 명령이 있으면 꺼내서 처리
            if not self.command_queue.empty():
                data = self.command_queue.get()        # 예: {"source":"GUI","cmd":"LEFT"}
                source = data.get("source", "")        # 명령 보낸 주체: "GUI" / "OPENCV"
                cmd = data.get("cmd", "")              # 명령 내용: "LEFT" 등 또는 AUTO일 때 error(float)

                # 1-1) 모드 전환 및 정지 (공통 처리)
                if isinstance(cmd, str):
                    u_cmd = cmd.upper()

                    # (A) 모드 전환: AUTO / MANUAL
                    if u_cmd in ["AUTO", "MANUAL"]:
                        self.control_mode = u_cmd
                        # 모드 전환 시 안전을 위해 일단 정지
                        self.current_lin_vel = 0.0
                        self.current_ang_vel = 0.0
                        print(f"[MODE] {self.control_mode}")
                        continue  # 모드 전환했으면 아래 로직은 스킵

                    # (B) STOP: 즉시 정지
                    if u_cmd == "STOP":
                        self.current_lin_vel = 0.0
                        self.current_ang_vel = 0.0
                        # NOTE: 여기서 continue가 없어서 아래 분기로 내려갈 수도 있음
                        #       안전하게 하려면 continue를 넣는 게 일반적으로 더 좋음

                # 1-2) 모드별 로직 분기
                # (MANUAL + GUI 입력) -> 버튼 명령으로 속도 누적 변경
                if self.control_mode == "MANUAL" and source == "GUI":
                    self.apply_manual_command(cmd)

                # (AUTO + OPENCV 입력) -> OpenCV가 준 라인 중심 오차(error)로 조향 계산
                elif self.control_mode == "AUTO" and source == "OPENCV":
                    # cmd에 선의 중심 오차(float/int)가 들어있다고 가정
                    try:
                        error = float(cmd)
                        self.current_lin_vel = self.auto_speed
                        # 오차에 비례해서 각속도 만들기(P 제어)
                        self.current_ang_vel = -(error * self.p_gain)
                    except ValueError:
                        # 숫자로 변환 안 되면 무시
                        pass

            # 2) 큐에 입력이 “없으면” 부드럽게 감속
            else:
                self.smooth_stop_linear()
                self.smooth_stop_angular()

            # 3) 속도 제한(clamp)
            self.current_lin_vel = max(-self.MAX_LIN, min(self.MAX_LIN, self.current_lin_vel))
            self.current_ang_vel = max(-self.MAX_ANG, min(self.MAX_ANG, self.current_ang_vel))

            # 4) 최종 publish (/cmd_vel)
            self.publisher.publish_cmd_vel(self.current_lin_vel, self.current_ang_vel)

            # 5) 루프 주기 (0.05초 = 20Hz)
            time.sleep(0.05)

    # ---------------------------------
    # 수동 모드 명령 처리
    #  - GUI에서 들어온 문자열(cmd)에 따라 속도를 조금씩 누적
    # ---------------------------------
    def apply_manual_command(self, cmd: str):
        if cmd == "GO":
            self.current_lin_vel += self.lin_step
        elif cmd == "BACK":
            self.current_lin_vel -= self.lin_step
        elif cmd == "LEFT":
            self.current_ang_vel += self.ang_step
        elif cmd == "RIGHT":
            self.current_ang_vel -= self.ang_step

    # ---------------------------------
    # OpenCV 라인 인식 스레드
    #  - AUTO 모드일 때만 카메라 영상으로 라인 중심 오차를 계산해서 큐로 넣음
    # ---------------------------------
    def opencv_thread(self):
        print("[RobotSystem] 터틀봇 카메라 스타트")

        # 카메라 구독 시작(rosbridge 쪽에서 이미지 수신 시작)
        self.publisher.subscribe_camera()

        while self.is_running:
            # AUTO일 때만 영상처리해서 error를 만들고 큐에 넣음
            if self.control_mode == "AUTO":
                # RosbridgePublisher가 보관하는 최신 프레임(가정)
                frame = self.publisher.latest_image

                if frame is None:
                    time.sleep(0.1)   # 아직 이미지가 안 오면 대기
                    continue

                # ---------- 영상 처리 ----------
                img = frame.copy()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # 임계값 이진화
                # - 검은 선이면 THRESH_BINARY_INV를 쓰면 선이 흰색으로 뒤집혀서 검출하기 쉬움
                _, thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY_INV)

                h, w = thresh.shape

                # 화면 하단 1/3만 ROI로 사용(바닥 라인만 보려고)
                roi = thresh[int(2 * h / 3):h, :]

                # 모멘트로 “흰색(선) 영역의 무게중심” 계산
                M = cv2.moments(roi)

                if M["m00"] > 0:
                    # 중심 x좌표(cx) = (x의 합 / 면적)
                    cx = int(M["m10"] / M["m00"])

                    # 화면 중앙(w/2) 대비 오차
                    # +면 선이 오른쪽, -면 선이 왼쪽
                    result = cx - (w / 2)

                    # 큐에 오차값 전송(AUTO 제어는 이걸 받아서 각속도로 변환)
                    self.command_queue.put({"source": "OPENCV", "cmd": result})
                else:
                    # 선을 못 찾으면 0을 보내서 “각속도 0” / 또는 감속 유도
                    self.command_queue.put({"source": "OPENCV", "cmd": 0})

                # 디버그 화면(PC에서만 의미 있음)
                cv2.imshow("Auto View", thresh)
                cv2.waitKey(1)

            else:
                # MANUAL 모드면 영상처리 안 하고 쉬기
                time.sleep(0.1)

        # NOTE: cap.release()는 여기선 cap을 안 쓰니까 호출하면 에러날 수 있음
        # cv2.destroyAllWindows() 정도가 더 맞을 수 있음
        # cv2.destroyAllWindows()

    # ---------------------------------
    # 스레드 시작 함수
    # ---------------------------------
    def start_threads(self):
        # main_controller 스레드 실행
        threading.Thread(target=self.main_controller, daemon=True).start()

        # opencv_thread 스레드 실행
        threading.Thread(target=self.opencv_thread, daemon=True).start()