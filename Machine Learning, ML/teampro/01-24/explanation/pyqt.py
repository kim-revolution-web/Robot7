import sys, os
from PyQt6 import uic
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class WidgetSample(QWidget):
    def __init__(self, robot_instance):
        super().__init__()

        # [핵심] robot 인스턴스를 받아서 저장
        # → 버튼 누르면 robot.command_queue에 dict 명령을 넣을 수 있다.
        self.robot = robot_instance

        # Qt Designer로 만든 main.ui 로드
        uic.loadUi(os.path.join(BASE_DIR, "main.ui"), self)

        # UI 버튼 objectName → 실제 로봇에 보낼 cmd 문자열 매핑
        # (main.ui 안 버튼의 objectName이 left/right/go/back... 이어야 동작)
        self.mapping = {
            "left":   "LEFT",
            "right":  "RIGHT",
            "go":     "GO",
            "back":   "BACK",
            "stop":   "STOP",
            "auto1":  "AUTO",
            "manual": "MANUAL",
        }

        # ---- "누르고 있는 동안 계속" 전송하기 위한 타이머 ----
        # 20Hz = 0.05초마다 한 번 send_command 실행
        self.hz = 20
        self.timer = QTimer(self)
        self.timer.setInterval(int(1000 / self.hz))
        self.timer.timeout.connect(self._tick_send)

        # 현재 누르고 있는 명령(예: "LEFT")을 저장
        self.active_cmd = None

        # 계속 누를 때 반복 전송할 버튼들
        hold_buttons = ["left", "right", "go", "back"]

        for obj_name in hold_buttons:
            btn = self.findChild(QPushButton, obj_name)
            if not btn:
                continue

            cmd = self.mapping[obj_name]

            # pressed: 누르는 순간 -> 반복 전송 시작
            btn.pressed.connect(lambda c=cmd: self._start_hold(c))
            # released: 손 떼면 -> 반복 전송 종료
            btn.released.connect(self._stop_hold)

        # STOP 버튼: 클릭하면 즉시 STOP 1회 + 타이머 종료
        stop_btn = self.findChild(QPushButton, "stop")
        if stop_btn:
            stop_btn.clicked.connect(self._stop_now)

        # AUTO / MANUAL 버튼: 클릭하면 1회만 전송
        for obj_name in ["auto1", "manual"]:
            btn = self.findChild(QPushButton, obj_name)
            if not btn:
                continue

            cmd = self.mapping[obj_name]
            btn.clicked.connect(lambda checked=False, c=cmd: self.send_command(c))

        self.show()

    # ---------------- 반복 전송 로직 ----------------
    def _start_hold(self, cmd: str):
        # "누르고 있는 동안" 보낼 명령을 저장
        self.active_cmd = cmd

        # 타이머가 안 돌고 있으면 시작
        if not self.timer.isActive():
            self.timer.start()

        # 누르는 순간 1번 바로 전송(반응 빠르게)
        self.send_command(cmd)

    def _stop_hold(self):
        # 손 떼면 타이머 멈추고 active_cmd 제거
        self.timer.stop()
        self.active_cmd = None
        # 필요하면 손 뗄 때 STOP 한 번 보내게 할 수도 있음
        # self.send_command("STOP")

    def _stop_now(self):
        # STOP은 즉시 정지
        self.timer.stop()
        self.active_cmd = None
        self.send_command("STOP")

    def _tick_send(self):
        # 타이머가 울릴 때마다 active_cmd를 반복 전송
        if self.active_cmd is not None:
            self.send_command(self.active_cmd)

    # ---------------- 실제 전송 함수 ----------------
    def send_command(self, cmd: str):
        print("GUI", cmd)  # 디버그 출력

        # [핵심] GUI → robot.command_queue로 dict를 넣어서 "명령 전달"
        # robot.py의 main_controller가 여기서 꺼내어 처리한다.
        if self.robot and self.robot.command_queue:
            self.robot.command_queue.put({'source': 'GUI', 'cmd': cmd})

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 단독 실행 시 robot 없이 실행하면 send_command에서 robot이 None이라 동작이 제한됨
    w = WidgetSample(robot_instance=None)
    sys.exit(app.exec())
