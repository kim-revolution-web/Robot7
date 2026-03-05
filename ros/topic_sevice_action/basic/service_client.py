import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class MinimalServiceClient(Node):
    def __init__(self):
        super().__init__('minimal_service_client')

        # (1) 서비스 클라이언트 생성 (서버의 서비스 이름과 동일해야 함)
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')

        # (2) 서버가 뜰 때까지 잠깐 기다림
        while not self.cli.wait_for_service(timeout_sec=0.5):
            self.get_logger().info('Waiting for /add_two_ints ...')

    def call(self, a: int, b: int):
        # (3) 요청 메시지 생성
        req = AddTwoInts.Request()
        req.a = a
        req.b = b

        # (4) 비동기 호출 (future 반환)
        future = self.cli.call_async(req)
        return future

def main():
    rclpy.init()
    node = MinimalServiceClient()

    # 예시로 3 + 5 요청
    future = node.call(3, 5)

    # (5) 응답 올 때까지 spin(이벤트 처리)
    rclpy.spin_until_future_complete(node, future)

    # (6) 응답 결과 확인
    if future.result() is not None:
        res = future.result()
        node.get_logger().info(f'Result: sum={res.sum}')
    else:
        node.get_logger().error(f'Service call failed: {future.exception()}')

    node.destroy_node()
    rclpy.shutdown()
