import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from example_interfaces.action import Fibonacci

class MinimalActionClient(Node):
    def __init__(self):
        super().__init__('minimal_action_client')

        # (1) 액션 클라이언트 생성 (서버의 액션 이름과 동일)
        self.client = ActionClient(self, Fibonacci, 'fibonacci')

    def send_goal(self, order: int):
        # (2) goal 메시지 생성
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        # (3) 서버가 준비될 때까지 대기
        self.client.wait_for_server()

        # (4) goal 전송 (feedback 콜백 등록 가능)
        self.get_logger().info(f'Send goal: order={order}')
        return self.client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_cb
        )

    def feedback_cb(self, feedback_msg):
        # (5) 진행 중 피드백 받는 곳
        partial = feedback_msg.feedback.partial_sequence
        self.get_logger().info(f'Feedback recv: {partial}')

def main():
    rclpy.init()
    node = MinimalActionClient()

    # 예시: order=10
    send_future = node.send_goal(10)

    # (6) goal 응답(수락/거절) 올 때까지 spin
    rclpy.spin_until_future_complete(node, send_future)
    goal_handle = send_future.result()

    if not goal_handle.accepted:
        node.get_logger().error('Goal rejected')
        node.destroy_node()
        rclpy.shutdown()
        return

    node.get_logger().info('Goal accepted')

    # (7) 최종 결과 요청
    result_future = goal_handle.get_result_async()

    # (8) 결과 올 때까지 spin (그 사이 feedback_cb가 계속 호출될 수 있음)
    rclpy.spin_until_future_complete(node, result_future)
    result = result_future.result().result

    node.get_logger().info(f'Final result: {result.sequence}')

    node.destroy_node()
    rclpy.shutdown()
