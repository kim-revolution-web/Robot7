"""robot_mover.py

[역할]
- ROS2 Node("robot_mover")로 동작하며 /cmd_vel 토픽에 geometry_msgs/Twist를 publish 한다.
- GUI에서 들어오는 GO/BACK/LEFT/RIGHT/STOP 명령을
  '속도 누적 방식'으로 변환해서 로봇을 움직인다.

[파일 간 연결]
- robot.py의 RobotSystem.execute_motor()가 여기의 move_robot()/stop()을 호출한다.
- Twist 메시지는 TurtleBot(또는 diff-drive 로봇) 기본 속도 제어 토픽인 /cmd_vel을 사용한다.

[현재 구현 특징]
- 버튼을 한 번 누르면 속도가 step 만큼 '누적'됨
  - GO  : linear.x += lin_step
  - BACK: linear.x -= lin_step
  - LEFT: angular.z += ang_step
  - RIGHT: angular.z -= ang_step
- 속도는 MAX_LIN, MAX_ANG 범위를 넘지 않도록 clamp(제한)한다.
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class RobotMover(Node):
    def __init__(self):
        # Node 이름: ros2 node list에 robot_mover로 보임
        super().__init__('robot_mover')

        # /cmd_vel 토픽으로 Twist 메시지를 publish
        # - queue size 10: 메시지 버퍼
        self.velocity_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # publish할 Twist 메시지 객체(매번 새로 만들지 않고 재사용)
        self.move_cmd = Twist()

        # ---------------- 현재 상태(누적 값) ----------------
        # 실시간 속도 누적값을 저장해두고, 버튼 입력에 따라 조금씩 변화
        self.current_lin_vel = 0.0   # 선속도(linear.x) m/s
        self.current_ang_vel = 0.0   # 각속도(angular.z) rad/s

        # ---------------- 한 번 입력 시 변화량(step) ----------------
        self.lin_step = 0.02  # 선속도 0.02 m/s 씩 증감
        self.ang_step = 0.1   # 각속도 0.1 rad/s 씩 증감

        # ---------------- 최대 제한(안전) ----------------
        # TurtleBot3 Burger 기준 최대값과 비슷하게 잡혀 있음(환경에 맞게 조절)
        self.MAX_LIN = 0.22
        self.MAX_ANG = 2.84

    def move_robot(self, command):
        """명령(command)에 따라 누적 속도를 변경하고 /cmd_vel로 publish"""

        # NOTE: RobotSystem에서 대문자로 보낼 수 있지만,
        #       안전하게 여기서도 한 번 더 통일
        command = command.upper()

        if command == "GO":
            # 앞으로 가는 속도를 누적(+ 방향)
            self.current_lin_vel += self.lin_step

        elif command == "BACK":
            # 뒤로 가는 속도를 누적(- 방향)
            self.current_lin_vel -= self.lin_step

        elif command == "LEFT":
            # 왼쪽 회전 속도를 누적(+ 방향)
            self.current_ang_vel += self.ang_step

        elif command == "RIGHT":
            # 오른쪽 회전 속도를 누적(- 방향)
            self.current_ang_vel -= self.ang_step

        elif command == "STOP":
            # 즉시 정지(누적값 리셋)
            self.current_lin_vel = 0.0
            self.current_ang_vel = 0.0

        # ---------------- 안전장치(클램핑) ----------------
        # 속도가 최대치를 넘지 않도록 제한
        self.current_lin_vel = max(-self.MAX_LIN, min(self.MAX_LIN, self.current_lin_vel))
        self.current_ang_vel = max(-self.MAX_ANG, min(self.MAX_ANG, self.current_ang_vel))

        # 변경된 누적 속도를 실제 토픽으로 전송
        self.publish_velocity()

    def publish_velocity(self):
        """현재 누적 속도를 Twist 메시지에 담아서 publish"""

        # Twist에 속도값을 채운다
        self.move_cmd.linear.x = float(self.current_lin_vel)
        self.move_cmd.angular.z = float(self.current_ang_vel)

        # 실제 publish
        self.velocity_pub.publish(self.move_cmd)

        print(f"[누적 상태] 선속도: {self.current_lin_vel:.2f} m/s | 각속도: {self.current_ang_vel:.2f} rad/s")

    def stop(self):
        """긴급 정지(외부에서 STOP을 강제할 때 사용)"""
        self.current_lin_vel = 0.0
        self.current_ang_vel = 0.0
        self.publish_velocity()
        print("[EMERGENCY STOP]")
