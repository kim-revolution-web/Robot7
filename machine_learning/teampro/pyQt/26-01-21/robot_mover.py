import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class RobotMover(Node):
    def __init__(self):
        super().__init__('robot_mover')
        self.velocity_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.move_cmd = Twist()
        # [현재 상태] 로봇의 실시간 속도값을 저장
        self.current_lin_vel = 0.0
        self.current_ang_vel = 0.0

        # [변동 단위] 한 번 누를 때마다 변할 양 (Step)
        self.lin_step = 0.02  # 0.02 m/s 씩 증감
        self.ang_step = 0.1   # 0.1 rad/s 씩 증감

        # [제한 값] 하드웨어 보호를 위한 마지노선
        self.MAX_LIN = 0.22
        self.MAX_ANG = 2.84

    def move_robot(self, command):
        """
        버튼을 누를 때마다 기존 속도에 값을 '더하거나 빼서' 누적시킵니다.
        """
        if command == "GO":
            # 앞으로 가는 속도를 누적 (+방향)
            self.current_lin_vel += self.lin_step
        elif command == "BACK":
            # 뒤로 가는 속도를 누적 (-방향)
            self.current_lin_vel -= self.lin_step

        elif command == "LEFT":
            # 왼쪽 회전 속도를 누적 (+방향)
            self.current_ang_vel += self.ang_step
        elif command == "RIGHT":
            # 오른쪽 회전 속도를 누적 (-방향)
            self.current_ang_vel -= self.ang_step

        elif command == "STOP":
            # 즉시 정지
            self.current_lin_vel = 0.0
            self.current_ang_vel = 0.0

        # 속도가 최대치를 넘지 않도록 안전장치(Clamping)
        self.current_lin_vel = max(-self.MAX_LIN, min(self.MAX_LIN, self.current_lin_vel))
        self.current_ang_vel = max(-self.MAX_ANG, min(self.MAX_ANG, self.current_ang_vel))

        # 최종 명령 전송
        self.publish_velocity()

    def publish_velocity(self):
        # 로봇에 전송할 값을 담는 과정
        self.move_cmd.linear.x = float(self.current_lin_vel)
        self.move_cmd.angular.z = float(self.current_ang_vel)
        
        #실제로 로봇에게 전송하는 부분
        self.velocity_pub.publish(self.move_cmd)

        print(f"[누적 상태] 선속도: {self.current_lin_vel:.2f} m/s | 각속도: {self.current_ang_vel:.2f} rad/s")

    def stop(self):
        self.current_lin_vel = 0.0
        self.current_ang_vel = 0.0
        self.publish_velocity()
        print("[EMERGENCY STOP]")