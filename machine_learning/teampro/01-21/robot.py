"""robot.py

[역할]
- RobotSystem: 전체 로봇 동작의 '중앙 허브'.
  - GUI/센서/카메라 등 여러 소스에서 들어오는 명령을 command_queue로 모아 처리한다.
  - control_mode(AUTO/MANUAL)에 따라 어떤 명령을 실행할지 제한한다.
  - ROS2(rclpy) 초기화 및 RobotMover(Node) 생성/스핀을 관리한다.

[파일 간 연결]
- pyqt.py(WidgetSample) → RobotSystem.command_queue 로 dict 명령을 넣음
  예: {"source": "GUI", "cmd": "LEFT"}
- robot_mover.py(RobotMover) → ROS2 토픽 '/cmd_vel'에 Twist를 publish하여 실제 이동 수행

[스레드 구조]
- sensor()        : 센서 기반 긴급정지(예: 장애물) 생성
- camera()        : AUTO 모드에서 자율주행 명령 생성(예: FOLLOW_PATH)
- main_controller(): command_queue에서 명령 꺼내서 execute_motor()로 실행
- rclpy.spin(...) : RobotMover(Node)의 ROS 콜백 처리(필수)
"""

import rclpy
import threading
import time
from queue import Queue

# 실제 이동(/cmd_vel publish) 담당 Node
from robot_mover import RobotMover


class RobotSystem:
    def __init__(self):
        # 전체 스레드 루프를 계속 돌릴지 여부
        self.is_running = True

        # 현재 제어 모드: GUI에서 MANUAL/AUTO로 전환
        # - MANUAL: GUI 명령(LEFT/RIGHT/GO/BACK/STOP 등)을 그대로 실행
        # - AUTO  : 카메라/자율주행 명령 중심으로 실행(센서 STOP은 항상 우선)
        self.control_mode = "MANUAL"  # "MANUAL" <-> "AUTO"

        # 여러 입력( GUI / SENSOR / CAMERA )을 한 곳으로 모으는 큐
        # dict 예시: {'source': 'GUI', 'cmd': 'LEFT'}
        self.command_queue = Queue()

        # ROS2 초기화: rclpy가 아직 init 안 된 상태면 여기서 초기화
        if not rclpy.ok():
            rclpy.init()

        # RobotMover는 ROS2 Node이면서 /cmd_vel publish를 담당
        self.mover = RobotMover()

    # ---------------- 1) 센서 스레드 ----------------
    def sensor(self):
        """예: 라이다/초음파 등 센서로 장애물 감지 → STOP 같은 긴급 명령 생성"""
        while self.is_running:
            # TODO: 실제 센서 값으로 교체
            obstacle_dist = 100  # (cm) 시뮬레이션 값

            # 전방 30cm 이내 장애물 감지 시 긴급 STOP
            if obstacle_dist < 30:
                # priority 필드는 지금 main_controller에서 사용하진 않지만,
                # 나중에 '우선순위 큐'로 바꿀 때 활용 가능
                self.command_queue.put({'source': 'SENSOR', 'cmd': 'STOP', 'priority': 1})

            time.sleep(0.1)  # 센서 주기(10Hz 정도)

    # ---------------- 2) 카메라 스레드(AUTO용) ----------------
    def camera(self):
        """AUTO 모드에서 비전 결과로 주행 명령 생성(현재는 더미)"""
        while self.is_running:
            if self.control_mode == "AUTO":
                # TODO: 실제로는 영상 처리 후 방향 결정(예: LEFT/RIGHT/GO 등)
                self.command_queue.put({'source': 'CAMERA', 'cmd': 'FOLLOW_PATH', 'priority': 2})

            time.sleep(0.2)  # 카메라/비전은 센서보다 느린 주기로(5Hz)

    # ---------------- 3) 메인 제어 스레드 ----------------
    def main_controller(self):
        """큐에 쌓인 명령을 꺼내서 실제 모터 동작으로 실행"""
        print("--- 프로그램 시작 ---")
        print(f"현재 모드: {self.control_mode}")

        while self.is_running:
            if not self.command_queue.empty():
                data = self.command_queue.get()

                # 어떤 소스에서 온 명령인지
                source = data.get('source')

                # 명령 문자열을 대문자로 통일
                action = data.get('cmd').upper() if data.get('cmd') else ""

                # 1) 모드 전환(AUTO/MANUAL)은 최우선 처리
                if action in ["AUTO", "MANUAL"]:
                    self.execute_motor(action)
                    continue

                # 2) 센서 기반 긴급 정지 or STOP 명령은 항상 최우선
                if source == 'SENSOR' or action == 'STOP':
                    self.execute_motor('STOP')
                    continue

                # 3) 현재 모드에 따라 실행 제약
                if self.control_mode == "MANUAL":
                    # MANUAL 모드: GUI 명령을 그대로 실행
                    # - LEFT/RIGHT/GO/BACK
                    self.execute_motor(action)

                elif self.control_mode == "AUTO":
                    # AUTO 모드: 보통 CAMERA 기반 명령만 실행하도록 제한할 수 있음
                    # 지금 코드는 주석 처리되어 있어 '모든 action'을 실행하고 있음
                    # if source == 'CAMERA':
                    self.execute_motor(action)

            time.sleep(0.01)  # CPU 과점유 방지

    # ---------------- 실제 동작(모드/이동) 실행 ----------------
    def execute_motor(self, action):
        action = action.upper()

        # 1) 모드 전환
        if action in ["AUTO", "MANUAL"]:
            self.control_mode = action
            print(f"\n[MODE] {self.control_mode}")
            return

        # 2) 이동/정지 명령 처리
        if action == "STOP":
            print("[System] STOP")
            self.mover.stop()

        elif action in ["GO", "BACK", "LEFT", "RIGHT"]:
            print(f"[System] {action}")

            # RobotMover가 속도를 '누적'시키는 방식이라,
            # 같은 명령을 여러 번 보내면 속도가 점점 증가/감소한다.
            self.mover.move_robot(action)

        else:
            # FOLLOW_PATH 같은 명령은 RobotMover에서 처리 로직이 없으면 아무 일도 안함
            # (필요하면 여기서 FOLLOW_PATH를 LEFT/RIGHT/GO로 변환하는 로직을 추가)
            print(f"[System] 알 수 없는 명령: {action}")

    # ---------------- 스레드 시작 ----------------
    def start_threads(self):
        """RobotSystem을 구성하는 스레드들을 데몬 스레드로 실행"""
        threading.Thread(target=self.sensor, daemon=True).start()
        threading.Thread(target=self.camera, daemon=True).start()
        threading.Thread(target=self.main_controller, daemon=True).start()

        # RobotMover(Node)는 ROS2 콜백 처리를 위해 spin이 필요
        threading.Thread(target=lambda: rclpy.spin(self.mover), daemon=True).start()
