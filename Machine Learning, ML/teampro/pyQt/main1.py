import sys, os
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton
from PyQt6 import uic

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class WidgetSample(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(BASE_DIR, "main1.ui"), self)

        # (선택) 전체 스타일 적용
        self.setStyleSheet("""
        QPushButton { background:#2d6cdf; color:white; border-radius:12px; padding:10px; font-weight:bold; }
        QPushButton:hover { background:#1f4fa8; }
        QPushButton:pressed { background:#173a7a; }
        """)

        # 버튼-명령 매핑
        mapping = {
            "up":   "UP",
            "down": "DOWN",
            "left": "LEFT",
            "right":"RIGHT",
            "stop": "STOP",
            "go":   "GO",
            "back": "BACK",
            "auto1": "AUTO",
        }

        # 연결: 클릭 시 send_command가 실행되게
        for obj_name, cmd in mapping.items():
            btn = self.findChild(QPushButton, obj_name)
            if btn:
                btn.clicked.connect(lambda checked=False, c=cmd: self.send_command(c))

        self.show()

    def send_command(self, cmd: str):
        print("COMMAND:", cmd)
        # TODO: 여기서 로봇/서버로 전송하면 됨
        # 예) serial.write((cmd+"\n").encode())
        # 예) socket.sendall(cmd.encode())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = WidgetSample()
    sys.exit(app.exec())