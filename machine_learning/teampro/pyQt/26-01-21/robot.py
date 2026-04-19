import rclpy
import threading
import time
from queue import Queue
from robot_mover import RobotMover

class RobotSystem:
    def __init__(self):
        self.is_running = True
        self.control_mode = "MANUAL"  # "MANUAL" <-> "AUTO"
        self.command_queue = Queue()
        
        if not rclpy.ok():
            rclpy.init()
        self.mover = RobotMover()

    # 1. 센서
    def sensor(self):
        while self.is_running:
            # 예: LiDAR에서 전방 30cm 이내 장애물 감지 시
            obstacle_dist = 100 # 시뮬레이션 값
            if obstacle_dist < 30:
                self.command_queue.put({'source': 'SENSOR', 'cmd': 'STOP', 'priority': 1})
            time.sleep(0.1)

    # 2. 카메라 (자율주행 명령)
    def camera(self):
        while self.is_running:
            if self.control_mode == "AUTO":
                # 실제로는 영상 처리 후 방향 결정 (L/R/F)
                self.command_queue.put({'source': 'CAMERA', 'cmd': 'FOLLOW_PATH', 'priority': 2})
            time.sleep(0.2) # 자율주행 주기는 센서보다 조금 여유있게

    # 3. 메인 이동 처리부
    def main_controller(self):
        print("--- 프로그램 시작 ---")
        print(f"현재 모드: {self.control_mode}")

        while self.is_running:
            if not self.command_queue.empty():
                data = self.command_queue.get()
                source = data.get('source')
                action = data.get('cmd').upper() if data.get('cmd') else ""

                # 1. 모드 전환 명령 (가장 먼저 처리)
                if action in ["AUTO", "MANUAL"]:
                    self.execute_motor(action)
                    continue

                # 2. 센서에 의한 긴급 정지
                if source == 'SENSOR' or action == 'STOP':
                    self.execute_motor('STOP')
                    continue

                # 3. 현재 설정된 모드에 따른 실행 제약
                if self.control_mode == "MANUAL":
                    # GUI나 다른 곳에서 온 수동 조작 명령 실행
                    self.execute_motor(action)

                elif self.control_mode == "AUTO":
                    # 자율주행 모드일 때는 카메라 명령만 실행 (혹은 센서)
                    #if source == 'CAMERA':
                    self.execute_motor(action)

            time.sleep(0.01)

    def execute_motor(self, action):
        action = action.upper()  # 대소문자 통일

       # 1. 모드 전환
        if action in ["AUTO", "MANUAL"]:
            self.control_mode = action
            print(f"\n[MODE] {self.control_mode}")
            return

        # 2. 실제 mover의 함수를 실행합니다.
        if action == "STOP":
            print("[System] STOP")
            self.mover.stop()
        elif action in ["GO", "BACK", "LEFT", "RIGHT"]:
            print(f"[System] {action}")
            self.mover.move_robot(action)  


    def start_threads(self):
        threading.Thread(target=self.sensor, daemon=True).start()
        threading.Thread(target=self.camera, daemon=True).start()
        threading.Thread(target=self.main_controller, daemon=True).start()
        threading.Thread(target=lambda: rclpy.spin(self.mover), daemon=True).start()
