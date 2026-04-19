"""main_code.py

[역할]
- 프로그램 진입점(entry point).
- ROS2 기반 로봇 시스템(RobotSystem)을 만들고(백그라운드 스레드 + ROS spin),
  PyQt6 GUI(WidgetSample)를 띄워서 GUI → RobotSystem으로 명령을 전달한다.

[파일 간 연결]
- pyqt.py : UI(main.ui)를 읽어서 버튼 이벤트를 처리하고, RobotSystem.command_queue로 명령(dict)을 넣는다.
- robot.py : RobotSystem(명령 큐/모드/스레드/ROS 초기화)을 관리한다.
- robot_mover.py : ROS2 Node로 /cmd_vel(Twist)을 publish 해서 실제 이동을 만든다.
"""

import sys
from PyQt6.QtWidgets import QApplication

# 같은 폴더(~/work/pyQt6) 안의 pyqt.py 파일에서 WidgetSample 클래스를 가져옴
from pyqt import WidgetSample

# 같은 폴더의 robot.py 파일에서 RobotSystem 클래스를 가져옴
from robot import RobotSystem

# ⚠ 현재 main_code.py에서는 RobotMover를 직접 쓰진 않지만,
#    robot.py 안에서 RobotMover(=robot_mover.py)가 실제 이동 publish를 담당한다.
from robot_mover import RobotMover  # (미사용 import라면 지워도 됨)


if __name__ == "__main__":
    # 1) PyQt 앱 객체 생성(필수)
    app = QApplication(sys.argv)

    # 2) 로봇 시스템 생성
    #    - 내부에서 rclpy.init() (필요시) 수행
    #    - RobotMover(Node) 생성
    #    - command_queue(Queue) 생성
    robot = RobotSystem()

    # 3) RobotSystem 내부 스레드 시작
    #    - sensor 스레드(장애물 감지 → STOP 같은 긴급명령)
    #    - camera 스레드(AUTO일 때 자율주행 명령 생성)
    #    - main_controller 스레드(큐에서 명령 꺼내서 mover로 실행)
    #    - rclpy.spin 스레드(ROS 콜백 처리)
    robot.start_threads()

    # 4) GUI 생성
    #    - WidgetSample(robot)로 "로봇 인스턴스"를 GUI에 주입
    #    - GUI는 버튼을 누르면 robot.command_queue.put({...}) 형태로 명령을 전달
    gui = WidgetSample(robot)

    # 5) GUI 화면 표시
    gui.show()

    # 6) Qt 이벤트 루프 시작(프로그램이 여기서 계속 실행됨)
    sys.exit(app.exec())
