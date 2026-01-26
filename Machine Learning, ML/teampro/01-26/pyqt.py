import sys, os
from PyQt6 import uic
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton

"""
==================== [이 파일(pyqt.py) 사용 설명] ====================

✅ 1) 이 pyqt.py는 "main.ui"를 로드해서 GUI를 띄웁니다.

✅ 2) UI에 이미 있는 라벨 2개를 그대로 씁니다.
   - 속도 라벨 objectName: "label"    (현재 UI에 name="label" 로 되어있음)
     예) Speed : 0.00  <-- 여기 텍스트를 계속 바꿔줌
   - 도형 라벨 objectName: "lblShape" (현재 UI에 name="lblShape")

✅ 3) 실제 프로젝트에서 어떤 파일에 어떤 값을 넣어야 화면에 표시되나?

   (A) robot.py (RobotSystem) 쪽에서 아래 값이 있어야 속도가 뜸
       - self.current_lin_vel  : 현재 선속도 (float)
       - self.current_ang_vel  : 현재 각속도 (float)
       - self.control_mode     : "AUTO" / "MANUAL"

   (B) 도형 인식(카메라/AI) 코드에서 아래 값을 넣어야 도형이 뜸
       - robot.current_shape = "TRIANGLE" / "SQUARE" / "CIRCLE" / "X"

   ✅ 이 pyqt.py는 0.1초마다(robot 값을 읽어서) 라벨 텍스트를 갱신합니다.
      그래서 다른 코드에서 robot.current_* 값만 바꿔주면 자동으로 화면에 표시됩니다.

✅ 4) 단독 실행 테스트
   - RobotSystem 없이도 실행되게 DummyRobot을 만들어서,
     시작 도형을 TRIANGLE로 두고 1초마다 SQUARE, CIRCLE로 바뀌게 데모를 넣어둠.

=====================================================================
"""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class WidgetSample(QWidget):
    def __init__(self, robot_instance):
        super().__init__()
        self.robot = robot_instance
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

        # ---------------- 누르고 있는 동안 반복 전송용 ----------------
        self.hz = 20  # 20Hz = 0.05초마다
        self.timer = QTimer(self)
        self.timer.setInterval(int(1000 / self.hz))
        self.timer.timeout.connect(self._tick_send)
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

        # ==========================================================
        # ✅ [도형/속도 표시 부분] (주석처리 X, 설명 주석 O)
        # ==========================================================
        # UI에 있는 라벨을 그대로 사용한다.
        #  - 속도 라벨 objectName="label"  → self.label 로 접근 가능
        #  - 도형 라벨 objectName="lblShape" → self.lblShape 로 접근 가능
        #
        # 아래 status_timer가 0.1초마다 robot 값을 읽어서 라벨 텍스트를 업데이트 한다.
        self.status_timer = QTimer(self)
        self.status_timer.setInterval(100)  # 100ms = 10Hz
        self.status_timer.timeout.connect(self._refresh_status)
        self.status_timer.start()

        self.show()

    # ---------------- 상태 표시 갱신 ----------------------------------------------
    def _refresh_status(self):
        """
        여기서 robot의 값을 읽어와서 UI 라벨에 표시한다.

        ✅ 실제 로봇에서 쓰려면 robot.py / camera.py 등에서 아래 변수들을 계속 갱신해야 함:
          - robot.current_lin_vel
          - robot.current_ang_vel
          - robot.control_mode
          - robot.current_shape
        """
        mode = getattr(self.robot, "control_mode", "-")
        lin = float(getattr(self.robot, "current_lin_vel", 0.0))
        ang = float(getattr(self.robot, "current_ang_vel", 0.0))
        shape = getattr(self.robot, "current_shape", "-")

        # UI의 속도 라벨(name="label") 텍스트 갱신
        # UI에서 name이 "label"이라서 self.label 로 바로 접근됨
        if hasattr(self, "Speed"):
            self.Speed.setText(f"Speed : {lin:.2f}  ang:{ang:.2f}  mode:{mode}")

        if hasattr(self, "Shape"):
            self.Shape.setText(f"Shape: {shape}")
#-------------------------------------------------------------------------------

    # ---------------- 반복 전송 로직 ----------------
    def _start_hold(self, cmd: str):
        self.active_cmd = cmd
        if not self.timer.isActive():
            self.timer.start()
        self.send_command(cmd)

    def _stop_hold(self):
        self.timer.stop()
        self.active_cmd = None

    def _stop_now(self):
        self.timer.stop()
        self.active_cmd = None
        self.send_command("STOP")

    def _tick_send(self):
        if self.active_cmd is not None:
            self.send_command(self.active_cmd)

    # ---------------- 실제 전송 함수 ----------------
    def send_command(self, cmd: str):
        print("GUI", cmd)
        if getattr(self.robot, "command_queue", None) is not None:
            self.robot.command_queue.put({'source': 'GUI', 'cmd': cmd})


# ===================== 단독 실행용 =====================
if __name__ == "__main__":
    import queue

    class DummyRobot:
        """
        ✅ RobotSystem 없이도 GUI만 테스트하려고 만든 더미 로봇

        실제 프로젝트에서는 DummyRobot 대신 robot.py의 RobotSystem 인스턴스를 넣으면 됨.
        """
        def __init__(self):
            self.command_queue = queue.Queue()

            # ✅ 속도/모드/도형 표시용 값(실제 프로젝트에서는 robot.py가 갱신)
            self.control_mode = "AUTO"
            self.current_lin_vel = 0.08
            self.current_ang_vel = 0.00

            # ✅ 처음 도형은 TRIANGLE로 시작
            self.current_shape = "TRIANGLE"

    robot = DummyRobot()

    app = QApplication(sys.argv)
    w = WidgetSample(robot)

    # ✅ 도형을 TRIANGLE -> SQUARE -> CIRCLE 로 1초마다 변경(테스트용)
    demo_shapes = ["TRIANGLE", "SQUARE", "CIRCLE"]
    idx = {"i": 0}

    def demo_change_shape():
        idx["i"] = (idx["i"] + 1) % len(demo_shapes)
        robot.current_shape = demo_shapes[idx["i"]]

        # 속도도 같이 변하는 것처럼 보이게 약간 바꿔줌(테스트용)
        robot.current_lin_vel = 0.05 + 0.03 * idx["i"]
        robot.current_ang_vel = 0.10 * idx["i"]

    demo_timer = QTimer()
    demo_timer.setInterval(1000)
    demo_timer.timeout.connect(demo_change_shape)
    demo_timer.start()

    # ✅ 큐에 들어오는 명령을 콘솔에 출력(버튼 동작 확인용)
    def poll_queue():
        while not robot.command_queue.empty():
            msg = robot.command_queue.get()
            print("[DUMMY ROBOT] got:", msg)

            cmd = msg.get("cmd", "").upper()
            if cmd in ["AUTO", "MANUAL"]:
                robot.control_mode = cmd  #  단독 실행에서도 모드 변경

    t = QTimer()
    t.setInterval(50)
    t.timeout.connect(poll_queue)
    t.start()

    sys.exit(app.exec())