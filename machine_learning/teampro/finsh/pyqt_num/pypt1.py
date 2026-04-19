import os
from PyQt6.QtWidgets import QWidget, QPushButton
from PyQt6 import uic

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class WidgetSample(QWidget):
    def __init__(self, robot_instance): # 로봇 인스턴스를 외부에서 받음
        super().__init__()
        self.robot = robot_instance
        uic.loadUi(os.path.join(BASE_DIR, "main.ui"), self) # ui파일을 가져옴

        # 버튼 매핑 "ui에 저장된 변수 : 출력되는 값"
        mapping = {
            "up": "UP", "down": "DOWN", "left": "LEFT",
            "right": "RIGHT", "stop": "STOP", "go": "GO",
            "back": "BACK", "auto1": "AUTO", "manual": "MANUAL",
        }

        for obj_name, cmd in mapping.items():
            btn = self.findChild(QPushButton, obj_name)
            if btn:
                btn.clicked.connect(lambda checked=False, c=cmd: self.send_command(c))

    def send_command(self, cmd: str):
        print(f"[GUI] 전송 명령: {cmd}")  # 확인용 로그
        self.robot.command_queue.put({'source': 'GUI', 'cmd': cmd})
