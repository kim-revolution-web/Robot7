"""pyqt.py

[역할]
- Qt Designer로 만든 UI 파일(main.ui)을 로드(uic.loadUi)해서 버튼 클릭/눌림 이벤트를 처리한다.
- 버튼 입력을 '문자 명령(cmd)'으로 바꾼 뒤, RobotSystem.command_queue로 전달한다.

[폴더/파일 연결]
- BASE_DIR = 이 파일(pyqt.py)이 있는 폴더 경로
- main.ui는 BASE_DIR 안에 있다고 가정하고 로드함
  → 즉, 기본 구조는 같은 폴더(~/work/pyQt6)에 pyqt.py, main.ui가 같이 있어야 함

[값(데이터) 전달 방식]
- GUI → RobotSystem(robot.py)으로 전달:
  self.robot.command_queue.put({"source": "GUI", "cmd": "LEFT"})
- 모드 변경(AUTO/MANUAL)은 두 방식 모두 적용:
  1) self.robot.control_mode 값을 직접 바꿈
  2) command_queue로도 동일 명령 dict을 넣어 다른 스레드가 알 수 있게 함
"""

import sys, os
from PyQt6 import uic
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton

# 이 파일(pyqt.py)의 "현재 위치(폴더)"를 기준으로 UI 파일을 찾기 위한 베이스 경로
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class WidgetSample(QWidget):
    def __init__(self, robot_instance, ui_file="main.ui", hz=20):
        """GUI 위젯 생성

        Args:
            robot_instance: robot.py의 RobotSystem 인스턴스(또는 동일 인터페이스를 가진 객체)
            ui_file: Qt Designer로 만든 .ui 파일명
            hz: 버튼을 누르고 있는 동안 같은 명령을 몇 Hz로 반복 전송할지(예: 20Hz)
        """
        super().__init__()

        # robot.py에서 만든 RobotSystem 인스턴스를 저장
        # → send_command()에서 self.robot.command_queue로 명령을 넣는다.
        self.robot = robot_instance

        # ---------------- 1) UI 로드 ----------------
        # main.ui를 현재 폴더(BASE_DIR)에서 찾아서 로드
        # 로드가 되면 UI 안의 objectName("left", "right" ...)을 self.findChild로 찾을 수 있음
        uic.loadUi(os.path.join(BASE_DIR, ui_file), self)

        # ---------------- 2) 버튼 이름(objectName) ↔ 명령(cmd) 매핑 ----------------
        # main.ui에서 버튼의 objectName과, 로봇에게 보낼 명령 문자열을 연결
        # ex) "left" 버튼을 누르면 "LEFT" cmd 전송
        self.mapping = {
            "left":   "LEFT",
            "right":  "RIGHT",
            "go":     "GO",
            "back":   "BACK",
            "stop":   "STOP",
            "auto1":  "AUTO",
            "manual": "MANUAL",
        }

        # ---------------- 3) "누르고 있는 동안 계속 전송"을 위한 타이머 ----------------
        # 예) 방향 버튼을 누른 채로 있으면 20Hz로 LEFT/RIGHT/GO/BACK을 계속 넣어줌
        self.active_cmd = None              # 현재 "누르고 있는" 명령(없으면 None)
        self.timer = QTimer(self)
        self.timer.setInterval(int(1000 / hz))  # ms 단위 → 20Hz면 50ms
        self.timer.timeout.connect(self._tick_send)

        # ---------------- 4) Hold 동작이 필요한 버튼들 ----------------
        # main.ui에 up/down이 없다고 해서 제외해둠
        hold_buttons = ["left", "right", "go", "back"]

        for obj_name in hold_buttons:
            # UI에서 objectName이 obj_name인 QPushButton 찾기
            btn = self.findChild(QPushButton, obj_name)
            if not btn:
                continue

            # 매핑에서 해당 버튼이 어떤 명령인지 가져오기
            cmd = self.mapping.get(obj_name)
            if not cmd:
                continue

            # pressed: 누르는 순간(마우스 다운) → 반복 전송 시작
            # released: 떼는 순간(마우스 업) → STOP 처리
            # ⚠ lambda 캡처 문제 방지를 위해 기본 인자(c=cmd)로 고정
            btn.pressed.connect(lambda c=cmd: self._start_hold(c))
            btn.released.connect(self._stop_hold)

        # ---------------- 5) STOP 버튼 ----------------
        # 클릭하면 즉시 STOP 1번 전송 + 타이머 중지(hold 해제)
        stop_btn = self.findChild(QPushButton, "stop")
        if stop_btn:
            stop_btn.clicked.connect(self._stop_now)

        # ---------------- 6) AUTO / MANUAL 버튼 ----------------
        # 클릭 1번으로 모드 전환 명령 전송(hold 아님)
        for obj_name in ["auto1", "manual"]:
            btn = self.findChild(QPushButton, obj_name)
            if not btn:
                continue
            cmd = self.mapping[obj_name]
            btn.clicked.connect(lambda checked=False, c=cmd: self.send_command(c))

    # ================= 반복 전송 로직 =================
    def _start_hold(self, cmd: str):
        """버튼을 누르는 순간 호출: 반복 전송 시작 + 즉시 1회 전송"""
        self.active_cmd = cmd
        if not self.timer.isActive():
            self.timer.start()

        # "누르는 순간" 바로 1번 보내서 반응을 빠르게
        self.send_command(cmd)

    def _stop_hold(self):
        """버튼을 떼는 순간 호출: STOP 처리"""
        self._stop_now()

    def _stop_now(self):
        """타이머 정지 + active_cmd 해제 + STOP 전송"""
        self.timer.stop()
        self.active_cmd = None
        self.send_command("STOP")

    def _tick_send(self):
        """타이머가 돌 때마다 호출: active_cmd를 계속 전송"""
        if self.active_cmd is not None:
            self.send_command(self.active_cmd)

    # ================= 로봇과 상호작용(핵심) =================
    def send_command(self, cmd: str):
        """GUI에서 만든 명령(cmd)을 RobotSystem으로 전달"""
        print(f"[GUI] 전송 명령: {cmd}")

        # 1) 모드 변경은 즉시 반영되도록 속성(control_mode)도 바꾸고
        #    큐에도 넣어서 main_controller가 처리할 수 있게 한다.
        if cmd in ("AUTO", "MANUAL"):
            if hasattr(self.robot, "control_mode"):
                self.robot.control_mode = cmd  # RobotSystem이 AUTO/MANUAL 상태를 즉시 알도록

            if hasattr(self.robot, "command_queue"):
                self.robot.command_queue.put({"source": "GUI", "cmd": cmd})
            return

        # 2) 이동/정지 명령: RobotSystem.command_queue로 전달
        #    RobotSystem.main_controller()가 큐를 읽어 RobotMover에 실행시킨다.
        if hasattr(self.robot, "command_queue"):
            self.robot.command_queue.put({"source": "GUI", "cmd": cmd})
        else:
            # command_queue가 없는 구현이라면,
            # 여기를 소켓/시리얼/ROS publish 등으로 바꾸면 된다.
            pass

    def closeEvent(self, event):
        """창 닫힐 때 호출됨 → 안전하게 STOP 보내고 종료"""
        self._stop_now()
        super().closeEvent(event)


# ---------------- 단독 테스트용(main_code.py 없이 GUI만 실행) ----------------
if __name__ == "__main__":
    class DummyRobot:
        """RobotSystem 대신 테스트용 더미"""
        def __init__(self):
            import queue
            self.command_queue = queue.Queue()
            self.control_mode = "MANUAL"

    robot = DummyRobot()

    app = QApplication(sys.argv)
    w = WidgetSample(robot_instance=robot, ui_file="main.ui", hz=20)
    w.show()
    sys.exit(app.exec())
