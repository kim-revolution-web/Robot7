import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts  # Request(a,b) / Response(sum)

class MinimalServiceServer(Node):
    def __init__(self):
        super().__init__('minimal_service_server')

        # (1) 서비스 서버 생성: 서비스 이름 'add_two_ints'
        self.srv = self.create_service(
            AddTwoInts,
            'add_two_ints',
            self.cb  # 요청이 오면 실행되는 콜백
        )

        self.get_logger().info('Service server ready: /add_two_ints')

    def cb(self, request: AddTwoInts.Request, response: AddTwoInts.Response):
        # (2) 요청값 접근
        a = request.a
        b = request.b

        # (3) 응답값 채우기
        response.sum = a + b

        # (4) 서버 로그
        self.get_logger().info(f'Request: a={a}, b={b} => sum={response.sum}')
        return response

def main():
    rclpy.init()
    node = MinimalServiceServer()

    # (5) 서버는 “항상 켜져 있어야” 요청을 받는다 → spin 유지
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()
