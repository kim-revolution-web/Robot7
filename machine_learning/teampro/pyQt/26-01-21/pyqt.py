import sys, os
from PyQt6 import uic
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class WidgetSample(QWidget):
    def __init__(self, robot_instance, ui_file="main.ui", hz=20):
        super().__init__()
        self.robot = robot_instance

        # UI 로드
        uic.loadUi(os.path.join(BASE_DIR, ui_file), self)

        # ui의 objectName -> 보낼 cmd (너 ui에 맞게 수정 가능)
        self.mapping = {
            "left":   "LEFT",
            "right":  "RIGHT",
            "go":     "GO",
            "back":   "BACK",
            "stop":   "STOP",
            "auto1":  "AUTO",
            "manual": "MANUAL",
        }

        # ---- 누르는 동안 반복 전송용 타이머 ----
        self.active_cmd = None
        self.timer = QTimer(self)
        self.timer.setInterval(int(1000 / hz))  # 예: 20Hz
        self.timer.timeout.connect(self._tick_send)

        # "누르고 있는 동안 계속" 할 버튼들 (up/down 없다고 했으니 제외)
        hold_buttons = ["left", "right", "go", "back"]

        for obj_name in hold_buttons:
            btn = self.findChild(QPushButton, obj_name)
            if not btn:
                continue

            cmd = self.mapping.get(obj_name)
            if not cmd:
                continue

            btn.pressed.connect(lambda c=cmd: self._start_hold(c))
            btn.released.connect(self._stop_hold)

        # STOP 버튼: 클릭하면 즉시 STOP 1번 + 타이머 종료
        stop_btn = self.findChild(QPushButton, "stop")
        if stop_btn:
            stop_btn.clicked.connect(self._stop_now)

        # AUTO / MANUAL: 클릭 1번 전송(모드 변경)
        for obj_name in ["auto1", "manual"]:
            btn = self.findChild(QPushButton, obj_name)
            if not btn:
                continue
            cmd = self.mapping[obj_name]
            btn.clicked.connect(lambda checked=False, c=cmd: self.send_command(c))

    # ---------------- 반복 전송 로직 ----------------
    def _start_hold(self, cmd: str):
        self.active_cmd = cmd
        if not self.timer.isActive():
            self.timer.start()

        # 누르는 순간 즉시 1번 전송(반응 빠르게)
        self.send_command(cmd)

    def _stop_hold(self):
        self._stop_now()

    def _stop_now(self):
        self.timer.stop()
        self.active_cmd = None
        self.send_command("STOP")

    def _tick_send(self):
        if self.active_cmd is not None:
            self.send_command(self.active_cmd)

    # ---------------- 로봇과 상호작용(여기가 핵심) ----------------
    def send_command(self, cmd: str):
        print(f"[GUI] 전송 명령: {cmd}")

        #  모드 명령은 robot 속성 변경 (너 로봇 코드에 맞춰 수정)
        if cmd in ("AUTO", "MANUAL"):
            # 예시: robot.control_mode가 있다면
            if hasattr(self.robot, "control_mode"):
                self.robot.control_mode = cmd
            # 또는 큐로도 보낼 수 있음
            if hasattr(self.robot, "command_queue"):
                self.robot.command_queue.put({"source": "GUI", "cmd": cmd})
            return

        #  이동/정지 명령은 큐로 전달
        if hasattr(self.robot, "command_queue"):
            self.robot.command_queue.put({"source": "GUI", "cmd": cmd})
        else:
            # 큐가 없으면 여기서 다른 방식(소켓/시리얼/ROS publish 등)으로 바꾸면 됨
            pass

    # 창 닫힐 때 안전 정지(추천)
    def closeEvent(self, event):
        self._stop_now()
        super().closeEvent(event)


# 예시 실행 (robot_instance는 네 실제 로봇 클래스 인스턴스로 교체)
if __name__ == "__main__":
    class DummyRobot:
        def __init__(self):
            import queue
            self.command_queue = queue.Queue()
            self.control_mode = "MANUAL"

    robot = DummyRobot()

    app = QApplication(sys.argv)
    w = WidgetSample(robot_instance=robot, ui_file="main.ui", hz=20)
    w.show()
    sys.exit(app.exec())