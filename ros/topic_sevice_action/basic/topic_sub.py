import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')

        # (1) 서브스크립션 생성: 같은 토픽 'chatter' 를 구독
        self.sub = self.create_subscription(
            String,
            'chatter',
            self.cb,   # 메시지 수신 시 실행할 콜백
            10
        )

    def cb(self, msg: String):
        # (2) msg.data 로 데이터 접근
        self.get_logger().info(f'Recv: {msg.data}')

def main():
    rclpy.init()
    node = MinimalSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
