import sys
from PyQt6.QtWidgets import QApplication

from pyqt import WidgetSample     # GUI(버튼) 담당
from robot import RobotSystem     # 로봇 제어(속도/큐/publish) 담당

if __name__ == "__main__":
    # 1) PyQt 앱(이벤트 루프) 생성
    app = QApplication(sys.argv)

    # 2) 로봇 제어 객체 생성
    robot = RobotSystem()

    # 3) 로봇 제어 스레드(main_controller) 시작
    robot.start_threads()

    # 4) GUI 생성 + robot 인스턴스를 주입(= GUI가 robot.command_queue로 명령을 넣을 수 있음)
    gui = WidgetSample(robot)
    gui.show()

    # 5) PyQt 이벤트 루프 실행
    sys.exit(app.exec())
