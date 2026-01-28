# robot.py
# -----------------------------------------
# 역할:
# - 로봇 제어의 "두뇌"
# - GUI / OpenCV 등에서 들어온 명령을 해석
# - 현재 속도 상태를 관리
# - 감속, 정지, 모드 전환 처리
# - 최종 속도 값을 link.py를 통해 로봇으로 전송
# -----------------------------------------

import time
import threading
from queue import Queue

from link import RosbridgePublisher


class RobotSystem:
    def __init__(self):
        # -------------------------------
        # 시스템 상태
        # -------------------------------
        self.is_running = True
        self.control_mode = "MANUAL"  # MANUAL / AUTO

        # 외부 입력(GUI, OpenCV 등)이 들어오는 큐
        self.command_queue = Queue()

        # 현재 로봇 속도 상태
        self.current_lin_vel = 0.0
        self.current_ang_vel = 0.0

        # 한 번 명령 시 증가/감소량
        self.lin_step = 0.005
        self.ang_step = 0.02

        # 최대 속도 제한 (하드웨어 보호)
        self.MAX_LIN = 0.15
        self.MAX_ANG = 1.0

        # 입력 없을 때 감속 비율
        self.lin_decel_rate = 0.002
        self.ang_decel_rate = 0.01

        # rosbridge 퍼블리셔
        self.publisher = RosbridgePublisher(
            ws_url="ws://192.168.0.68:9090"  # ← 로봇 IP
        )

    # ---------------------------------
    # 감속 처리 함수
    # ---------------------------------
    def smooth_stop_linear(self):
        if self.current_lin_vel > 0:
            self.current_lin_vel = max(
                0.0, self.current_lin_vel - self.lin_decel_rate
            )
        elif self.current_lin_vel < 0:
            self.current_lin_vel = min(
                0.0, self.current_lin_vel + self.lin_decel_rate
            )

    def smooth_stop_angular(self):
        if self.current_ang_vel > 0:
            self.current_ang_vel = max(
                0.0, self.current_ang_vel - self.ang_decel_rate
            )
        elif self.current_ang_vel < 0:
            self.current_ang_vel = min(
                0.0, self.current_ang_vel + self.ang_decel_rate
            )

    # ---------------------------------
    # 메인 제어 루프
    # ---------------------------------
    def main_controller(self):
        print("[RobotSystem] 제어 루프 시작")

        while self.is_running:
            if not self.command_queue.empty():
                data = self.command_queue.get()
                cmd = data.get("cmd", "").upper()

                # 모드 전환
                if cmd in ["AUTO", "MANUAL"]:
                    self.control_mode = cmd
                    print(f"[MODE] {self.control_mode}")
                    continue

                # 긴급 정지
                if cmd == "STOP":
                    self.current_lin_vel = 0.0
                    self.current_ang_vel = 0.0

                # 수동 조작
                elif self.control_mode == "MANUAL":
                    self.apply_manual_command(cmd)

            else:
                # 입력이 없으면 부드럽게 감속
                self.smooth_stop_linear()
                self.smooth_stop_angular()

            # 속도 제한 적용
            self.current_lin_vel = max(
                -self.MAX_LIN, min(self.MAX_LIN, self.current_lin_vel)
            )
            self.current_ang_vel = max(
                -self.MAX_ANG, min(self.MAX_ANG, self.current_ang_vel)
            )

            # 최종 속도 publish
            self.publisher.publish_cmd_vel(
                self.current_lin_vel,
                self.current_ang_vel
            )
            
            time.sleep(0.05)  # 20Hz

    # ---------------------------------
    # 수동 명령 처리
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
    # 스레드 시작
    # ---------------------------------
    def start_threads(self):
        threading.Thread(
            target=self.main_controller,
            daemon=True
        ).start()
