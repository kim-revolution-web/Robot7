import sys
from PyQt6.QtWidgets import QApplication
from pyqt import WidgetSample
from robot import RobotSystem
from robot_mover import RobotMover

if __name__ == "__main__":
    app = QApplication(sys.argv)

    

    robot = RobotSystem()
    robot.start_threads()

    gui = WidgetSample(robot)
    
    gui.show()

    sys.exit(app.exec())