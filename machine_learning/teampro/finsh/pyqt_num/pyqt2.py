import sys, os
from PyQt6 import uic
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class WidgetSample(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(BASE_DIR, "no_seed.ui"), self)

        # GUI 버튼 objectName -> 보낼 명령
        self.mapping = {

            "left":   "LEFT",
            "right":  "RIGHT",
            "go":     "GO",
            "back":   "BACK",
            "stop":   "STOP",
            "auto1":  "AUTO",
            "manual": "MANUAL",
        }

        # ✅ 누르고 있는 동안 반복 전송용
        self.hz = 20
        self.timer = QTimer(self)
        self.timer.setInterval(int(1000 / self.hz))
        self.timer.timeout.connect(self._tick_send)
        self.active_cmd = None  # 현재 누르고 있는 명령(UP/DOWN/...)

        # "누르고 있는 동안 계속" 할 버튼들
        hold_buttons = ["up", "down", "left", "right", "go", "back"]

        for obj_name in hold_buttons:
            btn = self.findChild(QPushButton, obj_name)
            if not btn:
                continue
            cmd = self.mapping[obj_name]

            # pressed: 시작
            btn.pressed.connect(lambda c=cmd: self._start_hold(c))
            # released: 정지
            btn.released.connect(self._stop_hold)

        # STOP 버튼: 누르면 즉시 STOP 1번 + 타이머 종료
        stop_btn = self.findChild(QPushButton, "stop")
        if stop_btn:
            stop_btn.clicked.connect(self._stop_now)

        # AUTO / MANUAL: 한 번 클릭하면 1번만 전송 (유지/토글은 별도)
        for obj_name in ["auto1", "manual"]:
            btn = self.findChild(QPushButton, obj_name)
            if not btn:
                continue
            cmd = self.mapping[obj_name]
            btn.clicked.connect(lambda checked=False, c=cmd: self.send_command(c))

        self.show()

    # ---------------- 반복 전송 로직 ----------------
    def _start_hold(self, cmd: str):
        self.active_cmd = cmd
        if not self.timer.isActive():
            self.timer.start()
        self.send_command(cmd)  # 누르는 순간 1번 바로 전송(반응 빠르게)

    def _stop_hold(self):
        self.timer.stop()
        self.active_cmd = None
        self.send_command("STOP")  # 손 떼면 정지 1번

    def _stop_now(self):
        self.timer.stop()
        self.active_cmd = None
        self.send_command("STOP")

    def _tick_send(self):
        if self.active_cmd is not None:
            self.send_command(self.active_cmd)

    # ---------------- 실제 전송 함수 ----------------
    def send_command(self, cmd: str):
        print("COMMAND:", cmd)
        # TODO: 여기서 로봇/서버로 전송
        # 예) serial.write((cmd+"\n").encode())
        # 예) socket.sendall(cmd.encode())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = WidgetSample()
    sys.exit(app.exec())
