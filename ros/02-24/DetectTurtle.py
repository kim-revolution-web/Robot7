import math

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, qos_profile_sensor_data
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class DetectTurtle(Node):
    def __init__(self):
        super().__init__('detect_turtle')

        self.stop_distance = 0.30  # m
        self.forward_speed = 0.20  # m/s
        self.turn_speed = 1.00     # rad/s
        self.back_speed = -0.10    # m/s  (뒤로 살짝)

        self.has_scan_received = False
        self.scan_msg = None

        self.cmd_vel_pub = self.create_publisher(
            Twist, '/cmd_vel', QoSProfile(depth=10)
        )

        self.scan_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            qos_profile=qos_profile_sensor_data
        )

        self.timer = self.create_timer(0.1, self.timer_callback)  # 10 Hz

    def scan_callback(self, msg: LaserScan):
        # scan 전체 메시지를 저장해야 angle_min, angle_increment도 쓸 수 있음
        self.scan_msg = msg
        self.has_scan_received = True

    def timer_callback(self):
        if self.has_scan_received and self.scan_msg is not None:
            self.detect_obstacle()

    def sector_min(self, deg1: float, deg2: float) -> float:
        """deg1~deg2(도) 구간의 유효 거리 중 최소값을 반환. 없으면 inf."""
        angle_min = self.scan_msg.angle_min
        inc = self.scan_msg.angle_increment
        ranges = self.scan_msg.ranges

        # 도 -> 라디안
        a1 = math.radians(deg1)
        a2 = math.radians(deg2)

        # 라디안 -> 인덱스
        i1 = int((a1 - angle_min) / inc)
        i2 = int((a2 - angle_min) / inc)

        # 인덱스 범위 보호
        n = len(ranges)
        i1 = max(0, min(i1, n - 1))
        i2 = max(0, min(i2, n - 1))
        if i1 > i2:
            i1, i2 = i2, i1

        # 유효값 필터(0, nan, inf 제거)
        valid = [r for r in ranges[i1:i2 + 1] if r > 0.0 and math.isfinite(r)]
        return min(valid) if valid else float('inf')

    def detect_obstacle(self):
        # 4분할(각 90도)
        front_min = self.sector_min(-45, 45)
        left_min = self.sector_min(45, 135)
        right_min = self.sector_min(-135, -45)
        back_min = min(self.sector_min(135, 180), self.sector_min(-180, -135))

        self.get_logger().info(
            f"front={front_min:.2f} left={left_min:.2f} right={right_min:.2f} back={back_min:.2f}",
            throttle_duration_sec=1.0
        )

        # 가장 위험한 방향(최소 거리)
        mins = {
            'front': front_min,
            'left': left_min,
            'right': right_min,
            'back': back_min
        }
        danger_dir = min(mins, key=mins.get)
        obstacle_distance = mins[danger_dir]

        twist = Twist()

        # 위험하면 회피, 아니면 전진
        if obstacle_distance < self.stop_distance:
            if danger_dir == 'front':
                # 앞이 위험하면: 후진(조금) + 직진(회전 0)
                twist.linear.x = self.back_speed
                twist.angular.z = 0.2
                self.get_logger().warn('Front dangerous -> backing up', throttle_duration_sec=2.0)

            elif danger_dir == 'left':
                # 왼쪽이 위험하면: 오른쪽으로 회전 (z 음수/양수는 환경에 따라 반대일 수 있음)
                twist.linear.x = 0.0
                twist.angular.z = -self.turn_speed
                self.get_logger().warn('Left dangerous -> turning right', throttle_duration_sec=2.0)

            elif danger_dir == 'right':
                # 오른쪽이 위험하면: 왼쪽으로 회전
                twist.linear.x = 0.0
                twist.angular.z = self.turn_speed
                self.get_logger().warn('Right dangerous -> turning left', throttle_duration_sec=2.0)

            else:  # 'back'
                # 뒤가 위험하면: 전진
                twist.linear.x = self.forward_speed
                twist.angular.z = 0.2
                self.get_logger().warn('Back dangerous -> moving forward', throttle_duration_sec=2.0)
        else:
            twist.linear.x = self.forward_speed
            twist.angular.z = 0.0

        self.cmd_vel_pub.publish(twist)


def main(args=None):
    rclpy.init(args=args)
    node = DetectTurtle()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard interrupt')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
