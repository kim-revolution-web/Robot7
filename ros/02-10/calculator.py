import time
from msg_srv_action_interface_example.msg import ArithmeticArgument

from rclpy.node import Node
from rclpy.qos import QoSDurabilityPolicy
from rclpy.qos import QoSHistoryPolicy
from rclpy.qos import QoSProfile
from rclpy.qos import QoSReliabilityPolicy
from rclpy.callback_groups import ReentrantCallbackGroup
import rclpy

from msg_srv_action_interface_example.srv import ArithmeticOperator

from msg_srv_action_interface_example.action import ArithmeticChecker
from rclpy.action import ActionServer
from rclpy.executors import MultiThreadedExecutor # 멀티 쓰레드

class Calculator(Node):

    def __init__(self):
        super().__init__('calculator')
        self.argument_a = 0.0
        self.argument_b = 0.0
        self.argument_operator = 0
        self.argument_result = 0.0
        self.argument_formula = ''
        self.operator = ['+', '-', '*', '/']
        self.callback_group = ReentrantCallbackGroup()
        self.declare_parameter('qos_depth', 10)
        qos_depth = self.get_parameter('qos_depth').value #초기값이 있는데 이렇게 쓰면 값을 바꿀수 있음

        QOS_RKL10V = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=qos_depth,
            durability=QoSDurabilityPolicy.VOLATILE)

        self.arithmetic_argument_subscriber = self.create_subscription(
            ArithmeticArgument,
            'arithmetic_argument',
            self.get_arithmetic_argument,
            QOS_RKL10V,
            callback_group=self.callback_group) #동시에 재진입

        self.arithmetic_service_server = self.create_service( #서비스는 기본 Qos 내부적으로 잡혀있음
            ArithmeticOperator,
            'arithmetic_operator',
            self.get_arithmetic_operator,
            callback_group=self.callback_group) #동시에 재진입

        self.arithmetic_action_server = ActionServer(
            self,
            ArithmeticChecker,
            'arithmetic_checker',
            self.execute_checker,
            callback_group=self.callback_group)


    def get_arithmetic_argument(self, msg):
      self.argument_a = msg.argument_a
      self.argument_b = msg.argument_b
      self.get_logger().info('Timestamp of the message: {0}'.format(msg.stamp))
      self.get_logger().info('Subscribed argument a: {0}'.format(self.argument_a))
      self.get_logger().info('Subscribed argument b: {0}'.format(self.argument_b))

#----------------------------------------------------------------------------
    def get_arithmetic_operator(self, request, response): #action 받는 부분
        self.argument_operator = request.arithmetic_operator

        self.argument_result = self.calculate_given_formula(
            self.argument_a,
            self.argument_b,
            self.argument_operator)

        response.arithmetic_result = self.argument_result

        self.argument_formula = '{0} {1} {2} = {3}'.format(
                self.argument_a,
                self.operator[self.argument_operator-1],
                self.argument_b,
                self.argument_result)

        self.get_logger().info(self.argument_formula)

        return response

    def calculate_given_formula(self, a, b, operator):
        if operator == ArithmeticOperator.Request.PLUS: #여기가 .srv에서 정의 한 값을 가져옴
            self.argument_result = a + b
        elif operator == ArithmeticOperator.Request.MINUS:
            self.argument_result = a - b
        elif operator == ArithmeticOperator.Request.MULTIPLY:
            self.argument_result = a * b
        elif operator == ArithmeticOperator.Request.DIVISION:
            try:
                self.argument_result = a / b
            except ZeroDivisionError:
                self.get_logger().error('ZeroDivisionError!')
                self.argument_result = 0.0
                return self.argument_result
        else:
            self.get_logger().error(
                'Please make sure arithmetic operator(plus, minus, multiply, division).')
            self.argument_result = 0.0
        return self.argument_result

#-----------------------------------------------------------------------------------
    ef execute_checker(self, goal_handle): #목표 핸들러?
        self.get_logger().info('Execute arithmetic_checker action!')

        feedback_msg = ArithmeticChecker.Feedback() #topic 응답이니까 response 같은 느낌?
        feedback_msg.formula = [] #list
        total_sum = 0.0
        goal_sum = goal_handle.request.goal_sum #goal_handle.request : 클라이언트가 보낸 Goal 메시지(여기선 goal_sum)

        while total_sum < goal_sum: #목표치 보다 적을 때만
            total_sum += self.argument_result #토탈에 결과값은 더해준다 .srv 에 들어있는 arithmetic_result?
            feedback_msg.formula.append(self.argument_formula) # argument_formula 지금  빈값인데  
            self.get_logger().info('Feedback: {0}'.format(feedback_msg.formula))
            goal_handle.publish_feedback(feedback_msg) #feedback은 server에서 주니까 
            time.sleep(1)

        goal_handle.succeed() #목표가 성공했나?

        result = ArithmeticChecker.Result() #결과 보내주고 받기?
        result.all_formula = feedback_msg.formula
        result.total_sum = total_sum #goal sum은 어디서 더해줘? Feedback은 topic이니깍 보내기만 하면 되고 Result는 어디서 보내고 어디서 받는거야? ,goal은 어디서 주고 받아?

        return result


def main(args=None):
    rclpy.init(args=args)
    try:
        calculator = Calculator()
        executor = MultiThreadedExecutor(num_threads=4)
        executor.add_node(calculator) #spain 매서드로 넣어주지 않고 직접 넣은거야?
        try:
            executor.spin()
        except KeyboardInterrupt:
            calculator.get_logger().info('Keyboard Interrupt (SIGINT)')
        finally:
            executor.shutdown()
            calculator.arithmetic_action_server.destroy()
            calculator.destroy_node()
    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()
