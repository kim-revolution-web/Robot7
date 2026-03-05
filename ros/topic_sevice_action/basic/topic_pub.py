import rclpy
from rclpy.node import Node
from std_msgs.msg import String  # 표준 String 메시지 타입

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')  # 노드 이름

        # (1) 퍼블리셔 생성: 토픽 이름 'chatter' 로 String 타입 발행
        self.pub = self.create_publisher(String, 'chatter', 10)  # 10 = 큐 depth (QoS)

        # (2) 주기적으로 publish 하려고 타이머 생성
        self.count = 0
        self.timer = self.create_timer(1.0, self.timer_cb)  # 1초마다 호출

    def timer_cb(self):
        # (3) 보낼 메시지 만들기
        msg = String()
        msg.data = f'hello {self.count}'
        self.count += 1

        # (4) publish
        self.pub.publish(msg)

        # (5) 로그 출력 (받는 쪽이 없어도 publish는 그냥 된다)
        self.get_logger().info(f'Publish: {msg.data}')

def main():
    rclpy.init()
    node = MinimalPublisher()

    # (6) spin: 콜백(timer_cb)이 계속 돌도록 이벤트 루프 유지
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()
