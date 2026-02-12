from action_msgs.msg import GoalStatus
from msg_srv_action_interface_example.action import ArithmeticChecker
from rclpy.action import ActionClient
from rclpy.node import Node
import argparse
import sys
import rclpy

class Checker(Node):

    def __init__(self):
        super().__init__('checker')
        self.arithmetic_action_client = ActionClient(
          self,
          ArithmeticChecker,
          'arithmetic_checker')


    def send_goal_total_sum(self, goal_sum):
        wait_count = 1
        while not self.arithmetic_action_client.wait_for_server(timeout_sec=0.1):  # 액션 서버가 준비될 때까지 잠깐씩 대기
            if wait_count > 3:
                self.get_logger().warning('Arithmetic action server is not available.') # warning은 info보다 "경고 레벨" 로그 (보통 색/레벨이 다르게 표시됨)
                return False
            wait_count += 1

        # Goal 메시지(클라이언트가 서버로 보내는 요청) 생성
        goal_msg = ArithmeticChecker.Goal()
        goal_msg.goal_sum = (float)(goal_sum)


        # Goal을 비동기로 전송
        self.send_goal_future = self.arithmetic_action_client.send_goal_async( # 서버 client에서 받는 부분
            goal_msg, #이형식으로 받고
            feedback_callback=self.get_arithmetic_action_feedback)# 서버가 publish_feedback() 할 때마다 여기로 들어옴
        self.send_goal_future.add_done_callback(self.get_arithmetic_action_goal) # send_goal_async의 done callback은 "Goal 응답(accepted/rejected)"을 받는 콜백
        return True


    def get_arithmetic_action_goal(self, future):# 여기 future.result()는 GoalHandle (Goal이 수락됐는지 등)를 담고 있음
        goal_handle = future.result()
        if not goal_handle.accepted: #수락 여부 확인
            self.get_logger().warning('Action goal rejected.')
            return
        self.get_logger().info('Action goal accepted.')
        # Goal이 accepted되면, 이제 Result를 비동기로 요청/대기
        self.action_result_future = goal_handle.get_result_async() #결과를 나중에 받기 위해 요청을 걸어두고 future를 받는 것
        self.action_result_future.add_done_callback(self.get_arithmetic_action_result)


    def get_arithmetic_action_feedback(self, feedback_msg): #msg 출력하는 애
        action_feedback = feedback_msg.feedback.formula
        self.get_logger().info('Action feedback: {0}'.format(action_feedback))


    def get_arithmetic_action_result(self, future): # feedback_msg는 래퍼(wrapper)라서 실제 데이터는 feedback_msg.feedback 안에 있음
          # future.result()는 "GetResult 응답" 객체이고,
        # 그 안에 status(상태코드)와 result(실제 Result 메시지)가 들어 있음
        action_status = future.result().status
        action_result = future.result().result
        if action_status == GoalStatus.STATUS_SUCCEEDED: ## GoalStatus.STATUS_SUCCEEDED는 "성공 완료" 상태 코드
            self.get_logger().info('Action succeeded!')
            self.get_logger().info(
                'Action result(all formula): {0}'.format(action_result.all_formula))# result string
            self.get_logger().info(
                'Action result(total sum): {0}'.format(action_result.total_sum))# result int
        else:
            self.get_logger().warning(
                'Action failed with status: {0}'.format(action_status))


def main(argv=sys.argv[1:]):   # sys.argv[0]는 "프로그램 이름"이라 보통 제외하고 실제 인자만 넘기려고 [1:]을 씀
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)#-h(help) 출력할 때 default 값도 같이 보여주게 하는 포맷터야

     # -g 또는 --goal_total_sum 옵션 인자를 받음
    parser.add_argument(
        '-g',
        '--goal_total_sum',
        type=int,
        default=50,
        help='Target goal value of total sum')

    # argparse가 모르는 인자(예: ROS의 --ros-args ...)를 남김 없이 argv에 담아두기 위한 장치
    # → 남은 인자를 rclpy.init에 그대로 넘기려고
    parser.add_argument(
        'argv', nargs=argparse.REMAINDER,
        help='Pass arbitrary arguments to the executable')
    args = parser.parse_args()


    # rclpy.init에는 "ROS용 인자들"을 넘길 수 있음 (--ros-args 등)
    rclpy.init(args=args.argv) #rclpy.init(args=args) 이렇게만 쓰는데 args=args.argv) 이건뭐야
    try:
        checker = Checker()
        checker.send_goal_total_sum(args.goal_total_sum)
        try:
            rclpy.spin(checker)
        except KeyboardInterrupt:
            checker.get_logger().info('Keyboard Interrupt (SIGINT)')
        finally:
            checker.arithmetic_action_client.destroy()#checker.destroy_node() 여기서 다 날라가는거 아니야? arithmetic_action_client따로 또 날려?
            checker.destroy_node()
    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()

