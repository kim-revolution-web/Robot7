# robot.py
# -----------------------------------------
# 역할:
# - 로봇 제어의 "두뇌"
# - GUI / OpenCV 등에서 들어온 명령을 해석
# - 현재 속도 상태를 관리
# - 모드 전환 처리
# - 최종 속도 값을 link.py를 통해 로봇(/cmd_vel)로 전송
# -----------------------------------------

from __future__ import annotations

import time
import threading
from queue import Queue
from typing import Optional

from link import RosbridgePublisher


class RobotSystem:
    def __init__(self):
        # -------------------------------
        # 시스템 상태
        # -------------------------------
        self.is_running = True
        self.control_mode = "MANUAL"  # "MANUAL" / "AUTO"

        # 외부 입력(GUI, Camera 등)이 들어오는 큐
        self.command_queue = Queue()

        # 현재 로봇 속도 상태
        self.current_lin_vel = 0.0
        self.current_ang_vel = 0.0

        # (GUI용) 도형 상태
        self.current_shape = "NONE"

        # -------------------------------
        # MANUAL 제어 설정
        # -------------------------------
        self.lin_step = 0.005
        self.ang_step = 0.05

        # -------------------------------
        # 속도 제한 (하드웨어 보호)
        # TurtleBot3 Burger 기준으로 안전한 범위로 설정
        # -------------------------------
        self.MAX_LIN = 0.22
        self.MAX_ANG = 2.84

        # 입력 없을 때 감속 비율(부드럽게)
        self.lin_decel_rate = 0.005
        self.ang_decel_rate = 0.050

        # -------------------------------
        # AUTO 제어 설정
        #   0~1 비율로 받고 실제 속도는 MAX_LIN에 스케일
        # -------------------------------
        self.auto_lin_ratio = 0.1  # 0~1
        self.auto_kp = 2.0         # error_norm(약 -1~+1) -> ang_z (rad/s)
        self.auto_deadzone_ratio = 0.02  # 정중앙 근처 데드존(비율)

        # -------------------------------
        # rosbridge 퍼블리셔
        # -------------------------------
        self.publisher = RosbridgePublisher(
            ws_url="ws://192.168.0.93:9090"  # ← 로봇 IP
        )

    # ---------------------------------
    # 감속 처리 함수
    # ---------------------------------
    def smooth_stop_linear(self):
        if self.current_lin_vel > 0:
            self.current_lin_vel = max(0.0, self.current_lin_vel - self.lin_decel_rate)
        elif self.current_lin_vel < 0:
            self.current_lin_vel = min(0.0, self.current_lin_vel + self.lin_decel_rate)

    def smooth_stop_angular(self):
        if self.current_ang_vel > 0:
            self.current_ang_vel = max(0.0, self.current_ang_vel - self.ang_decel_rate)
        elif self.current_ang_vel < 0:
            self.current_ang_vel = min(0.0, self.current_ang_vel + self.ang_decel_rate)

    # ---------------------------------
    # 속도 제한
    # ---------------------------------
    def clamp(self):
        self.current_lin_vel = max(-self.MAX_LIN, min(self.MAX_LIN, self.current_lin_vel))
        self.current_ang_vel = max(-self.MAX_ANG, min(self.MAX_ANG, self.current_ang_vel))

    # ---------------------------------
    # 메인 제어 루프
    # ---------------------------------
    def main_controller(self):
        print("[RobotSystem] 제어 루프 시작")

        while self.is_running:
            if not self.command_queue.empty():
                data = self.command_queue.get()
                cmd = str(data.get("cmd", "")).upper()

                # -------------------------
                # 모드 전환
                # -------------------------
                if cmd in ["AUTO", "MANUAL"]:
                    self.control_mode = cmd
                    # 모드 바뀔 때는 안전하게 0으로
                    self.current_lin_vel = 0.0
                    self.current_ang_vel = 0.0
                    continue

                # -------------------------
                # STOP (요청사항)
                # - AUTO일 때 STOP 누르면:
                #   1) 즉시 정지
                #   2) MANUAL로 전환
                # - MANUAL일 때 STOP 누르면:
                #   즉시 정지(모드는 유지)
                # -------------------------
                if cmd == "STOP":
                    self.current_lin_vel = 0.0
                    self.current_ang_vel = 0.0
                    if self.control_mode == "AUTO":
                        self.control_mode = "MANUAL"
                    # STOP은 여기서 끝
                    self._publish_once()
                    continue

                # -------------------------
                # AUTO 전용 정지(모드 유지)
                # -------------------------
                if cmd == "AUTO_STOP":
                    if self.control_mode == "AUTO":
                        self.current_lin_vel = 0.0
                        self.current_ang_vel = 0.0
                    self._publish_once()
                    continue

                # -------------------------
                # AUTO 라인트레이싱 입력
                # -------------------------
                if cmd == "AUTO_LINE":
                    if self.control_mode == "AUTO":
                        err_px = float(data.get("value", 0.0))

                        # err_px: 왼쪽(+) / 오른쪽(-)
                        # 정규화: 대략 -1~+1 범위
                        # (픽셀 기준은 카메라쪽에서 640기준 320 중심)
                        # 여기서는 320으로 나눠 정규화한다.
                        err_norm = err_px / 320.0

                        # 데드존
                        if abs(err_norm) < self.auto_deadzone_ratio:
                            ang = 0.0
                        else:
                            # error가 클수록 각속도 크게
                            ang = self.auto_kp * err_norm

                        # 고정 직진 속도(비율 -> 실제)
                        lin = float(self.auto_lin_ratio) * self.MAX_LIN

                        self.current_lin_vel = lin
                        self.current_ang_vel = ang
                    self.clamp()
                    self._publish_once()
                    continue

                # -------------------------
                # MANUAL 조작
                # (AUTO일 때는 무시해서 부담/오작동 방지)
                # -------------------------
                if self.control_mode == "MANUAL":
                    self.apply_manual_command(cmd)

            else:
                # 입력이 없으면 부드럽게 감속
                self.smooth_stop_linear()
                self.smooth_stop_angular()

            # 제한 + publish
            self.clamp()
            self.publisher.publish_cmd_vel(self.current_lin_vel, self.current_ang_vel)

            time.sleep(0.05)  # 20Hz

        # 루프 종료 시 정지
        try:
            self.publisher.publish_cmd_vel(0.0, 0.0)
            self.publisher.close()
        except Exception:
            pass

    def _publish_once(self):
        """명령 처리 직후 즉시 1회 publish(응답성)"""
        self.clamp()
        self.publisher.publish_cmd_vel(self.current_lin_vel, self.current_ang_vel)

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
        threading.Thread(target=self.main_controller, daemon=True).start()
