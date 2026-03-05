import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from example_interfaces.action import Fibonacci

class MinimalActionServer(Node):
    def __init__(self):
        super().__init__('minimal_action_server')

        # (1) 액션 서버 생성: 액션 이름 'fibonacci'
        self.server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            execute_callback=self.execute_cb  # goal 받으면 실제 수행하는 함수
        )

        self.get_logger().info('Action server ready: /fibonacci')

    def execute_cb(self, goal_handle):
        # (2) goal(요청) 값 확인
        order = goal_handle.request.order
        self.get_logger().info(f'Goal received: order={order}')

        # (3) 피드백/결과 객체 준비
        feedback = Fibonacci.Feedback()
        feedback.partial_sequence = [0, 1]

        # (4) “진행 중” 피드백을 여러 번 보내기 (action의 핵심)
        for i in range(2, order):
            # 취소 요청 들어왔는지 체크(최소 구성이라 간단히만)
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                result = Fibonacci.Result()
                result.sequence = feedback.partial_sequence
                return result

            feedback.partial_sequence.append(
                feedback.partial_sequence[i - 1] + feedback.partial_sequence[i - 2]
            )

            # 피드백 publish
            goal_handle.publish_feedback(feedback)
            self.get_logger().info(f'Feedback: {feedback.partial_sequence}')

            time.sleep(0.5)  # “작업이 진행 중”인 것처럼 딜레이

        # (5) 작업 완료 처리
        goal_handle.succeed()

        # (6) 최종 결과 반환
        result = Fibonacci.Result()
        result.sequence = feedback.partial_sequence
        self.get_logger().info(f'Result: {result.sequence}')
        return result

def main():
    rclpy.init()
    node = MinimalActionServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
