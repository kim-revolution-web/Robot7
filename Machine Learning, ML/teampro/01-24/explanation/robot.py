# robot.py
# 역할: 로봇 제어 "두뇌"
# - GUI(OpenCV 등)에서 들어온 명령을 해석
# - 현재 속도 상태를 갱신
# - 입력 없으면 감속(smooth stop)
# - 최종 /cmd_vel을 rosbridge로 publish(link.py)

import time
import threading
from queue import Queue
from link import RosbridgePublisher


class RobotSystem:
    def __init__(self):
        # 프로그램 계속 실행할지
        self.is_running = True

        # 제어 모드: MANUAL / AUTO
        self.control_mode = "MANUAL"

        # 외부 입력(GUI 등)이 여기에 dict로 들어온다.
        # 예: {'source':'GUI', 'cmd':'LEFT'}
        self.command_queue = Queue()

        # 현재 속도 상태(최종 publish 되는 값)
        self.current_lin_vel = 0.0
        self.current_ang_vel = 0.0

        # 수동 조작 시 한 번 누를 때마다 변화량
        self.lin_step = 0.005   # GO/BACK 누를 때 선속도 변화
        self.ang_step = 0.02    # LEFT/RIGHT 누를 때 각속도 변화

        # 속도 제한(로봇 보호)
        self.MAX_LIN = 0.15
        self.MAX_ANG = 1.0

        # 입력이 없을 때 서서히 멈추는 감속 비율
        self.lin_decel_rate = 0.002
        self.ang_decel_rate = 0.01

        # rosbridge에 연결해서 /cmd_vel publish 하는 객체
        self.publisher = RosbridgePublisher(
            ws_url="ws://192.168.0.68:9090"
        )

    # ---- 입력이 없으면 부드럽게 감속(선속도) ----
    def smooth_stop_linear(self):
        if self.current_lin_vel > 0:
            self.current_lin_vel = max(0.0, self.current_lin_vel - self.lin_decel_rate)
        elif self.current_lin_vel < 0:
            self.current_lin_vel = min(0.0, self.current_lin_vel + self.lin_decel_rate)

    # ---- 입력이 없으면 부드럽게 감속(각속도) ----
    def smooth_stop_angular(self):
        if self.current_ang_vel > 0:
            self.current_ang_vel = max(0.0, self.current_ang_vel - self.ang_decel_rate)
        elif self.current_ang_vel < 0:
            self.current_ang_vel = min(0.0, self.current_ang_vel + self.ang_decel_rate)

    # ---- 메인 제어 루프(핵심) ----
    def main_controller(self):
        print("[RobotSystem] 제어 루프 시작")

        while self.is_running:
            # 1) 큐에 명령이 있으면 꺼내서 처리
            if not self.command_queue.empty():
                data = self.command_queue.get()

                # NOTE: source(누가 보냈는지)는 현재 코드에선 사용하지 않음
                # source = data.get("source", "")

                # cmd를 대문자로 통일
                cmd = data.get("cmd", "").upper()

                # (A) 모드 전환
                if cmd in ["AUTO", "MANUAL"]:
                    self.control_mode = cmd
                    print(f"[MODE] {self.control_mode}")
                    continue

                # (B) 긴급 정지
                if cmd == "STOP":
                    self.current_lin_vel = 0.0
                    self.current_ang_vel = 0.0

                # (C) MANUAL일 때만 수동 명령 적용
                elif self.control_mode == "MANUAL":
                    self.apply_manual_command(cmd)

                # (D) AUTO 명령(AUTO_LEFT/AUTO_RIGHT 등)은
                # 현재 robot.py에는 처리 로직이 없다.
                # camera.py를 붙이려면 여기에 분기를 추가해야 함.

            else:
                # 2) 큐에 입력이 없으면 감속(천천히 0으로)
                self.smooth_stop_linear()
                self.smooth_stop_angular()

            # 3) 속도 제한(클램프)
            self.current_lin_vel = max(-self.MAX_LIN, min(self.MAX_LIN, self.current_lin_vel))
            self.current_ang_vel = max(-self.MAX_ANG, min(self.MAX_ANG, self.current_ang_vel))

            # 4) 최종 /cmd_vel publish (rosbridge로 전송)
            self.publisher.publish_cmd_vel(self.current_lin_vel, self.current_ang_vel)

            # 5) 20Hz 주기
            time.sleep(0.05)

    # ---- 수동 명령 처리 ----
    def apply_manual_command(self, cmd: str):
        if cmd == "GO":
            self.current_lin_vel += self.lin_step
        elif cmd == "BACK":
            self.current_lin_vel -= self.lin_step
        elif cmd == "LEFT":
            self.current_ang_vel += self.ang_step
        elif cmd == "RIGHT":
            self.current_ang_vel -= self.ang_step

    # ---- 스레드 시작 ----
    def start_threads(self):
        threading.Thread(target=self.main_controller, daemon=True).start()
