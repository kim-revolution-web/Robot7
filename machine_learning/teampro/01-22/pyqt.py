import sys, os
from PyQt6 import uic
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class WidgetSample(QWidget):
    def __init__(self, robot_instance): # 1. 로봇 받게 바꿈
        super().__init__()
        self.robot = robot_instance # 2. 로봇 저장
        uic.loadUi(os.path.join(BASE_DIR, "main.ui"), self)
        

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

        # 누르고 있는 동안 반복 전송용
        self.hz = 20 # 0.05 sec
        self.timer = QTimer(self)
        self.timer.setInterval(int(1000 / self.hz))
        self.timer.timeout.connect(self._tick_send)

        # 현재 누르고 있는 명령(UP/DOWN/...)
        self.active_cmd = None  

        # "누르고 있는 동안 계속" 할 버튼들
        hold_buttons = [ "left", "right", "go", "back"]

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

    # 누르다 땠을 때
    def _stop_hold(self):
        self.timer.stop()
        self.active_cmd = None
        #self.send_command("STOP")  # 손 떼면 정지 1번

    # stop 버튼을 누흠
    def _stop_now(self):
        self.timer.stop()
        self.active_cmd = None
        self.send_command("STOP")

    def _tick_send(self):
        if self.active_cmd is not None:
            self.send_command(self.active_cmd)

    # ---------------- 실제 전송 함수 ----------------
    def send_command(self, cmd: str):
        print("GUI", cmd) # 확인용
       
        if self.robot and self.robot.command_queue:
            self.robot.command_queue.put({'source': 'GUI', 'cmd': cmd})

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     w = WidgetSample()
#     sys.exit(app.exec())

# ---------------- pyqt.py + main.ui 단독 실행용 ----------------
if __name__ == "__main__":
    import queue

    class DummyRobot:
        """RobotSystem 없이 GUI만 테스트: command_queue만 제공"""
        def __init__(self):
            self.command_queue = queue.Queue()

    robot = DummyRobot()

    app = QApplication(sys.argv)
    w = WidgetSample(robot)   # robot_instance 넣어서 실행 (WidgetSample 안에서 self.show() 함)

    # 큐에 들어오는 명령을 콘솔에 출력(동작 확인용)
    def poll_queue():
        while not robot.command_queue.empty():
            print("[DUMMY ROBOT] got:", robot.command_queue.get())

    t = QTimer()
    t.setInterval(50)
    t.timeout.connect(poll_queue)
    t.start()

    sys.exit(app.exec())