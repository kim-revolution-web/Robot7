import sys, os
from PyQt6 import uic
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QProgressBar

"""
[어떤 파일에서 어떤 값을 적어야 하나?]

1) robot.py (RobotSystem)에서 아래 값이 계속 갱신되면 GUI가 자동 표시함
   - self.control_mode        : "AUTO" / "MANUAL"
   - self.current_lin_vel     : 선속도 (m/s)
   - self.current_ang_vel     : 각속도 (rad/s)
   - self.MAX_LIN             : 최대 선속도 (예: 0.15)
   - self.MAX_ANG             : 최대 각속도 (예: 1.0)

2) 도형 인식 코드(camera/AI)에서 아래처럼 갱신하면 도형 표시됨
   - robot.current_shape = "TRIANGLE" / "SQUARE" / "CIRCLE" / "X"

※ UI에서 라벨 objectName을 이렇게 해둬야 함
   - QLabel name="Speed"
   - QLabel name="Shape"
"""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class WidgetSample(QWidget):
    def __init__(self, robot_instance):
        super().__init__()
        self.robot = robot_instance

        # ✅ 먼저 UI 로드 (findChild 쓰려면 loadUi가 먼저!)
        uic.loadUi(os.path.join(BASE_DIR, "main.ui"), self)

        # ---------------- 버튼 -> 명령 매핑 ----------------
        self.mapping = {
            "left":   "LEFT",
            "right":  "RIGHT",
            "go":     "GO",
            "back":   "BACK",
            "stop":   "STOP",
            "auto1":  "AUTO",
            "manual": "MANUAL",
        }

        # ---------------- 누르고 있는 동안 반복 전송용(QTimer) ----------------
        self.hz = 20
        self.send_timer = QTimer(self)                       # ✅ 이름 바꿈(충돌 방지)
        self.send_timer.setInterval(int(1000 / self.hz))
        self.send_timer.timeout.connect(self._tick_send)
        self.active_cmd = None

        hold_buttons = ["left", "right", "go", "back"]
        for obj_name in hold_buttons:
            btn = self.findChild(QPushButton, obj_name)
            if not btn:
                continue
            cmd = self.mapping[obj_name]
            btn.pressed.connect(lambda c=cmd: self._start_hold(c))
            btn.released.connect(self._stop_hold)

        stop_btn = self.findChild(QPushButton, "stop")
        if stop_btn:
            stop_btn.clicked.connect(self._stop_now)

        for obj_name in ["auto1", "manual"]:
            btn = self.findChild(QPushButton, obj_name)
            if not btn:
                continue
            cmd = self.mapping[obj_name]
            btn.clicked.connect(lambda checked=False, c=cmd: self.send_command(c))

        # ---------------- 속도 ProgressBar 2개 생성 ----------------
        # UI에 라벨 Speed가 있으니, 그 아래쪽에 막대를 "코드로" 붙여넣음
        self._init_speed_bars()

        # ---------------- 상태 갱신 타이머(10Hz) ----------------
        self.status_timer = QTimer(self)
        self.status_timer.setInterval(100)
        self.status_timer.timeout.connect(self._refresh_status)
        self.status_timer.start()

        self.show()

    def _init_speed_bars(self):
        """
        robot.py의 MAX_LIN(0.15), MAX_ANG(1.0)을 기준으로
        현재 lin/ang를 %로 변환해서 보여줄 ProgressBar 2개
        """
        if not hasattr(self, "Speed"):
            return

        r = self.Speed.geometry()

        # 선속도 바
        self.pbar_lin = QProgressBar(self)
        self.pbar_lin.setGeometry(r.x(), r.y() + r.height() - 10, r.width(), 18)
        self.pbar_lin.setRange(0, 100)
        self.pbar_lin.setFormat("LIN  %p%")
        self.pbar_lin.setTextVisible(True)

        # 각속도 바 (선속도 바 바로 아래)
        self.pbar_ang = QProgressBar(self)
        self.pbar_ang.setGeometry(r.x(), r.y() + r.height() + 14, r.width(), 18)
        self.pbar_ang.setRange(0, 100)
        self.pbar_ang.setFormat("ANG  %p%")
        self.pbar_ang.setTextVisible(True)

        # 바 스타일(원하면 색 더 바꿔도 됨)
        self.pbar_lin.setStyleSheet("QProgressBar{border:1px solid #ccc;border-radius:6px;text-align:center;}"
                                    "QProgressBar::chunk{background:#2563eb;border-radius:6px;}")
        self.pbar_ang.setStyleSheet("QProgressBar{border:1px solid #ccc;border-radius:6px;text-align:center;}"
                                    "QProgressBar::chunk{background:#10b981;border-radius:6px;}")

        self.pbar_lin.raise_()
        self.pbar_ang.raise_()

    # ---------------- 상태 표시 갱신 ----------------
    def _refresh_status(self):
        mode = getattr(self.robot, "control_mode", "-")
        lin = float(getattr(self.robot, "current_lin_vel", 0.0))
        ang = float(getattr(self.robot, "current_ang_vel", 0.0))
        shape = getattr(self.robot, "current_shape", "-")

        max_lin = float(getattr(self.robot, "MAX_LIN", 0.15))
        max_ang = float(getattr(self.robot, "MAX_ANG", 1.0))

        # 라벨 업데이트
        if hasattr(self, "Speed"):
            self.Speed.setText(f"Speed : Lin {lin:.2f}/{max_lin:.2f}   Ang {ang:.2f}/{max_ang:.2f}   Mode {mode}")
        if hasattr(self, "Shape"):
            self.Shape.setText(f"Shape: {shape}")

        # ProgressBar 업데이트 (%)
        if hasattr(self, "pbar_lin"):
            lin_pct = int(min(100, max(0, (abs(lin) / max_lin) * 100))) if max_lin > 0 else 0
            self.pbar_lin.setValue(lin_pct)
        if hasattr(self, "pbar_ang"):
            ang_pct = int(min(100, max(0, (abs(ang) / max_ang) * 100))) if max_ang > 0 else 0
            self.pbar_ang.setValue(ang_pct)

    # ---------------- 반복 전송 로직 ----------------
    def _start_hold(self, cmd: str):
        self.active_cmd = cmd
        if not self.send_timer.isActive():
            self.send_timer.start()
        self.send_command(cmd)

    def _stop_hold(self):
        self.send_timer.stop()
        self.active_cmd = None

    def _stop_now(self):
        self.send_timer.stop()
        self.active_cmd = None
        self.send_command("STOP")

    def _tick_send(self):
        if self.active_cmd is not None:
            self.send_command(self.active_cmd)

    def send_command(self, cmd: str):
        print("GUI", cmd)
        if getattr(self.robot, "command_queue", None) is not None:
            self.robot.command_queue.put({'source': 'GUI', 'cmd': cmd})


# ===================== 단독 실행용 =====================
if __name__ == "__main__":
    import queue

    class DummyRobot:
        def __init__(self):
            self.command_queue = queue.Queue()

            self.control_mode = "AUTO"
            self.current_lin_vel = 0.0
            self.current_ang_vel = 0.0
            self.current_shape = "TRIANGLE"

            # 최대값 (robot.py랑 맞추기)
            self.MAX_LIN = 0.15
            self.MAX_ANG = 1.0

            # ✅ "누르고 있을 때 증가량"
            # robot.py랑 똑같이 쓰려면 아래 값 추천
            self.lin_step = 0.005     # 전진/후진 증가량
            self.ang_step = 0.02      # 좌/우 회전 증가량

            # 네가 말한 것처럼 0.05씩 올리고 싶으면 이렇게 바꿔도 됨(근데 금방 MAX 찍음)
            # self.lin_step = 0.05
            # self.ang_step = 0.02

        def clamp(self):
            self.current_lin_vel = max(-self.MAX_LIN, min(self.MAX_LIN, self.current_lin_vel))
            self.current_ang_vel = max(-self.MAX_ANG, min(self.MAX_ANG, self.current_ang_vel))

        def apply_cmd(self, cmd: str):
            # ✅ RobotSystem의 apply_manual_command랑 같은 역할 (단독 실행용)
            if cmd == "GO":
                self.current_lin_vel += self.lin_step
            elif cmd == "BACK":
                self.current_lin_vel -= self.lin_step
            elif cmd == "LEFT":
                self.current_ang_vel += self.ang_step
            elif cmd == "RIGHT":
                self.current_ang_vel -= self.ang_step
            elif cmd == "STOP":
                self.current_lin_vel = 0.0
                self.current_ang_vel = 0.0

            self.clamp()

    robot = DummyRobot()

    app = QApplication(sys.argv)
    w = WidgetSample(robot)

    # ✅ (옵션) 도형만 데모로 바뀌게
    demo_shapes = ["TRIANGLE", "SQUARE", "CIRCLE"]
    i = {"v": 0}

    def demo_shape_only():
        i["v"] = (i["v"] + 1) % 3
        robot.current_shape = demo_shapes[i["v"]]

    demo_timer = QTimer()
    demo_timer.setInterval(1000)
    demo_timer.timeout.connect(demo_shape_only)
    demo_timer.start()

    # ✅ GUI에서 들어오는 명령을 읽어서 DummyRobot 속도를 바꿈
    def poll_queue():
        while not robot.command_queue.empty():
            msg = robot.command_queue.get()
            cmd = msg.get("cmd", "").upper()
            print("[DUMMY ROBOT] got:", msg)

            if cmd in ["AUTO", "MANUAL"]:
                robot.control_mode = cmd
            else:
                # ✅ GO/BACK/LEFT/RIGHT/STOP 처리
                robot.apply_cmd(cmd)

    t = QTimer()
    t.setInterval(20)  # 50ms도 되지만, 좀 더 부드럽게 하려면 20ms
    t.timeout.connect(poll_queue)
    t.start()

    sys.exit(app.exec())