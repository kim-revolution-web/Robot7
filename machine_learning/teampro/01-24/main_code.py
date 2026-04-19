import sys
from PyQt6.QtWidgets import QApplication
from pyqt import WidgetSample 
from robot import RobotSystem 

if __name__ == "__main__":
    app = QApplication(sys.argv)

    robot = RobotSystem()
    robot.start_threads() 

    # 2. GUI 생성 및 로봇 연결
    gui = WidgetSample(robot) # 생성할 때 robot을 꼭 넣어줌
    gui.show()

    sys.exit(app.exec())
