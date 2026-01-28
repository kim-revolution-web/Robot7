import sys, os 
from PyQt6 import uic #.ui 파일 로드
from PyQt6.QtCore import QTimer #주기적으로 함수를 실행 #
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton



#import sys 시스템 모듈에서
#QApplication(sys.argv) : 실행 옵션(명령줄 인자) 전달
#sys.exit(app.exec()) : app.exec()에 들어있는 종료코드 os에 전달

#timer.timeout.connect(func)
#timer.start(200)ms

#QApplication
#app.exec() 로 이벤트 루프 시작

#QWidget
#화면 클래스가 QWidget(또는 QMainWindow)를 상속함
#있어야 gui가 뜸

#QPushButton
#btn.clicked.connect(handler)

#.connect()
#Qt의 Signal-Slot(이벤트 연결) 개념을 PyQt가 파이썬 문법으로 제공하는 거야.
#clicked, timeout 같은 건 “시그널(signal)”이고, 연결되는 함수는 “슬롯(slot)”이라고 불러.
"""
==================== [이 파일(pyqt.py) 사용 설명] ====================

1) 이 pyqt.py는 "main.ui"를 로드해서 GUI를 띄웁니다.

2) UI에 이미 있는 라벨 2개를 그대로 씁니다.  (너 UI 기준)
   - 속도 라벨 objectName: "Speed"
   - 도형 라벨 objectName: "Shape"
3) 실제 프로젝트에서 어떤 파일에 어떤 값을 넣어야 화면에 표시되나?

   (A) robot.py (RobotSystem) 쪽에서 아래 값이 계속 갱신되면 속도/모드가 뜸
       - self.current_lin_vel  : 현재 선속도(float)
       - self.current_ang_vel  : 현재 각속도(float)
       - self.control_mode     : "AUTO" / "MANUAL"

   (B) 카메라/AI 코드에서 아래 값을 갱신하면 도형이 뜸
       - robot.current_shape = "TRIANGLE" / "SQUARE" / "CIRCLE" / "X"

 4) 단독 실행 테스트
   - RobotSystem 없이도 실행되게 DummyRobot을 넣어둠
   - 1초마다 TRIANGLE/SQUARE/CIRCLE 데모 변경
   - 버튼을 누르면 DummyRobot 속도/모드도 실제로 바뀌게 구현(중요)

=====================================================================
"""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))# 현재 팡일 경로 


class WidgetSample(QWidget): #GUI 클래스(창/위젯)를 정의
    def __init__(self, robot_instance):
        super().__init__() #  Qt 위젯동작 필수 위젯(창) 초기화 
        self.robot = robot_instance # 외부에서 받은 로봇 객체를 저장해서 계속 사용

        #  UI 먼저 로드해야 findChild/Speed/Shape가 생김
        uic.loadUi(os.path.join(BASE_DIR, "main.ui"), self)

        # ---------------- 버튼 -> 명령 매핑 ----------------
        self.mapping = { #딕셔너리 구조
            "left":   "LEFT",
            "right":  "RIGHT",
            "go":     "GO",
            "back":   "BACK",
            "stop":   "STOP",
            "auto1":  "AUTO",
            "manual": "MANUAL",
        }

        # ---------------- 누르고 있는 동안 반복 전송용 ----------------
        self.hz = 20  #1초에 20번 실행 1/20초 = 50ms  
        self.send_timer = QTimer(self)  #타이머 객체를 생성 위젯이 정리되면 타이머도 꺼짐 
        self.send_timer.setInterval(int(1000 / self.hz)) #timout 시간을 어느정도 할지 ms값으로 받음
        self.send_timer.timeout.connect(self._tick_send) #끝날때 신호  50ms마다 _tick_send()실행 
        self.active_cmd = None  #  눌리고 있는 버튼이 없다

        # "누르고 있는 동안 계속" 할 버튼들
        hold_buttons = ["left", "right", "go", "back"]
        for obj_name in hold_buttons:
            btn = self.findChild(QPushButton, obj_name) #findChild 그 조건(타입+이름)인 위젯이 있나
            if not btn: # 예외 처리 
                continue
            cmd = self.mapping[obj_name] #mapping 값 가져오기  
            btn.pressed.connect(lambda c=cmd: self._start_hold(c)) #눌렸을 때 cmd를 c로 만들어서 현재값을 줌
            btn.released.connect(self._stop_hold) #떨어졌을때 _stop_hold 호출

        # STOP 버튼: 즉시 STOP 1번
        stop_btn = self.findChild(QPushButton, "stop")
        if stop_btn:
            stop_btn.clicked.connect(self._stop_now)

        # AUTO / MANUAL: 클릭 1번 전송
        for obj_name in ["auto1", "manual"]:
            btn = self.findChild(QPushButton, obj_name)
            if not btn:
                continue
            cmd = self.mapping[obj_name]
            btn.clicked.connect(lambda checked=False, c=cmd: self.send_command(c))
            # checked=False는 클릭 시 전달되는 기본 인자를 무시하기 위함

        # ---------------- 상태 갱신 타이머(10Hz) ----------------
        self.status_timer = QTimer(self)
        self.status_timer.setInterval(100)
        self.status_timer.timeout.connect(self._refresh_status) #100ms 마다 시간 초기화
        self.status_timer.start()

        self.show() #창 띄우기 

    # ---------------- 상태 표시 갱신 ----------------
    def _refresh_status(self):
        mode = getattr(self.robot, "control_mode", "-") 
        lin = float(getattr(self.robot, "current_lin_vel", 0.0))
        ang = float(getattr(self.robot, "current_ang_vel", 0.0))
        shape = getattr(self.robot, "current_shape", "-")

        #  UI 라벨 이름: Speed / Shape
        if hasattr(self, "Speed"): #hasattr speed 라벨 확인 
            self.Speed.setText(f"Speed : {lin:.2f}  ang:{ang:.2f}  mode:{mode}")#덱스트 표시 위젯
        if hasattr(self, "Shape"):
            self.Shape.setText(f"Shape: {shape}")

    # ---------------- 반복 전송 로직 ----------------
    def _start_hold(self, cmd: str):
        self.active_cmd = cmd
        if not self.send_timer.isActive():#isActive 타이머가 실행중인지 확인
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
        if self.active_cmd is not None: #행동할때
            self.send_command(self.active_cmd) #계속 전송

    # ---------------- 실제 전송 함수 ----------------
    def send_command(self, cmd: str): 
        print("GUI", cmd)# GUI에서 이런 명령 보냈다 출력
        if getattr(self.robot, "command_queue", None) is not None: #“robot 안에 command_queue가 있을 때만
            self.robot.command_queue.put({'source': 'GUI', 'cmd': cmd})  #GUI가 준 cmd를 큐에 넣는 것


# ===================== 단독 실행용 =====================
if __name__ == "__main__":
    import queue

    class DummyRobot:
        """RobotSystem 없이도 GUI만 테스트하려고 만든 더미 로봇"""
        def __init__(self):
            self.command_queue = queue.Queue() #명령을 쌓아둘 큐를 하나 만들겠다

            self.control_mode = "AUTO"
            self.current_lin_vel = 0.00
            self.current_ang_vel = 0.00
            self.current_shape = "TRIANGLE"

            #  단독 실행에서도 GO/LEFT 같은 걸 누르면 값이 바뀌게 step/limit 넣음
            self.lin_step = 0.005
            self.ang_step = 0.02
            self.MAX_LIN = 0.15
            self.MAX_ANG = 1.0

        def clamp(self):
            self.current_lin_vel = max(-self.MAX_LIN, min(self.MAX_LIN, self.current_lin_vel))
            self.current_ang_vel = max(-self.MAX_ANG, min(self.MAX_ANG, self.current_ang_vel))

        def apply_cmd(self, cmd: str):
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

    app = QApplication(sys.argv) #qt 앱 객체생성   
    w = WidgetSample(robot) #WidgetSample 위젯(창) 인스턴스를 만들면서, 생성자

    #  도형 데모(테스트용)
    demo_shapes = ["TRIANGLE", "SQUARE", "CIRCLE"]
    idx = {"i": 0}

    def demo_change_shape():
        idx["i"] = (idx["i"] + 1) % len(demo_shapes)
        robot.current_shape = demo_shapes[idx["i"]]

    demo_timer = QTimer()
    demo_timer.setInterval(1000)
    demo_timer.timeout.connect(demo_change_shape)
    demo_timer.start()

    #  큐에 들어오는 명령 처리(중요!)
    def poll_queue():
        while not robot.command_queue.empty(): #empty 신호가 
            msg = robot.command_queue.get()
            cmd = msg.get("cmd", "").upper()
            print("[DUMMY ROBOT] got:", msg)

            # 모드 변경
            if cmd in ["AUTO", "MANUAL"]:
                robot.control_mode = cmd
            else:
                #  단독 실행에서도 버튼 누르면 속도/각속도 값이 실제로 바뀜
                robot.apply_cmd(cmd)

    t = QTimer()
    t.setInterval(20)     # 50ms도 되지만 20ms가 더 부드러움
    t.timeout.connect(poll_queue)
    t.start()

    sys.exit(app.exec()) 
