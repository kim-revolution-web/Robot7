import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from std_srvs.srv import Trigger  # ✅ 서비스 타입

from rclpy.qos import QoSProfile, QoSDurabilityPolicy, QoSHistoryPolicy, QoSReliabilityPolicy
from rclpy.callback_groups import ReentrantCallbackGroup


class Move_turtle(Node):
    def __init__(self):
        super().__init__('move_turtle')

        self.declare_parameter('qos_depth', 10)
        qos_depth = self.get_parameter('qos_depth').value
        self.callback_group = ReentrantCallbackGroup()

        qos = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=qos_depth,
            durability=QoSDurabilityPolicy.VOLATILE
        )

        self.cmd_pub = self.create_publisher(
            Twist, '/cmd_vel', qos, callback_group=self.callback_group
        )

        # ✅ UI 토픽 구독
        self.ui_sub = self.create_subscription(
            String, 'ui_pub_sub', self.ui_cmd, qos, callback_group=self.callback_group
        )

        # ✅ STOP 서비스 서버
        self.stop_srv = self.create_service(
            Trigger, 'stop_service', self.on_stop_service, callback_group=self.callback_group
        )

        self.linear = 0.0
        self.angular = 0.0

        # ✅ 20Hz로 cmd_vel 계속 퍼블리시
        self.timer = self.create_timer(0.05, self.move_cmd_pub)

    def move_cmd_pub(self):
        msg = Twist()
        msg.linear.x = float(self.linear)
        msg.angular.z = float(self.angular)
        self.cmd_pub.publish(msg)

    def ui_cmd(self, msg: String):
        try:
            parts = msg.data.strip().split()
            self.linear = float(parts[0])
            self.angular = float(parts[1])
            self.get_logger().info(f"UI cmd received: linear={self.linear}, angular={self.angular}")
        except Exception:
            self.get_logger().warning(
                f"Bad ui_pub_sub format: '{msg.data}' (expected: '<linear> <angular>')"
            )

    # ✅ 서비스 콜백: 정지 + 즉시 publish + 응답
    def on_stop_service(self, request: Trigger.Request, response: Trigger.Response):
        self.linear = 0.0
        self.angular = 0.0

        # 즉시 1번 쏴서 체감 지연 제거
        self.move_cmd_pub()

        response.success = True
        response.message = "Stopped: cmd_vel published (linear=0, angular=0)"
        self.get_logger().info("STOP service called -> robot stopped.")
        return response


def main(args=None):
    rclpy.init(args=args)
    node = Move_turtle()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard interrupt!!!!')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
