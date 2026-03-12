import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from std_srvs.srv import Trigger


from rclpy.qos import QoSProfile, QoSDurabilityPolicy, QoSHistoryPolicy, QoSReliabilityPolicy
from rclpy.callback_groups import ReentrantCallbackGroup

class Move_turtle(Node):
  def __init__(self):
    super().__init__('move_turtle')
    self.declare_parameter('qos_depth', 10)
    qos_depth = self.get_parameter('qos_depth').value #현재값을 가져온다
    self.callback_group = ReentrantCallbackGroup()



    #self.add_on_set_parameters_callback(self.update_parameter) #변경을 감지해서 알려줌


    qos = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,#꼭 전달해라
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=qos_depth,
            durability=QoSDurabilityPolicy.VOLATILE)#과거는 잊고 현재 것만 준다

    self.cmd_pub= self.create_publisher(Twist, '/cmd_vel', qos,callback_group=self.callback_group)
    self.timer = self.create_timer(0.05, self.move_cmd_pub) #gui에서 받는 속도가 느려서0.05사용


    self.ui_sub = self.create_subscription(String, 'ui_pub_sub',self.ui_cmd,qos,callback_group=self.callback_group)

    self.linear = 0.0
    self.angular = 0.0



  def move_cmd_pub(self):
    msg = Twist()
    msg.linear.x = float(self.linear)
    msg.angular.z = float(self.angular)
    self.cmd_pub.publish(msg)

  def ui_cmd(self, msg: String):
        # msg.data 예: "0.4 -0.2"  (linear angular)
        try:
            parts = msg.data.strip().split()#split 공백 기준으로 list로 만들어줌
            self.linear = float(parts[0])
            self.angular = float(parts[1])
             # ✅ 즉시 1번 쏴서 반응 지연 제거
            # self.move_cmd_pub()


            self.get_logger().info(f"UI cmd received: linear={self.linear}, angular={self.angular}")
        except Exception:
            self.get_logger().warning(f"Bad ui_pub_sub format: '{msg.data}' (expected: '<linear> <angular>')")



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
