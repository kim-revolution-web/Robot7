import sys
from PyQt6.QtWidgets import QApplication
from pro0122.pyqt import WidgetSample 
from pro0122.robot import RobotSystem 


if __name__ == "__main__":
    app = QApplication(sys.argv)#Qt GUI “엔진”을 켜는 코드

    robot = RobotSystem()#RobotSystem 객체를 하나 만듦.
    robot.start_threads()#GUI는 버튼만 눌러주고 실제 “명령 처리/전송”은 이 스레드들이 담당.

    # 2. GUI 생성 및 로봇 연결
    gui = WidgetSample(robot) # 생성할 때 robot을 꼭 넣어줌
    gui.show()

    sys.exit(app.exec())#app.exec() : Qt 이벤트 루프 시작.
    #sys.exit(...) : 프로그램 종료 시 운영체제에 종료 코드를 전달.