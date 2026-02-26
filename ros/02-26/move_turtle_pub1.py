

from std_msgs.msg import String
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from rclpy.qos import QoSProfile
import termios
import tty
import os
import select
import sys

class Move_turtle(Node):
  def __init__(self):
    super().__init__('move_key_turtle')
    self.qos_profile = QoSProfile(depth = 10)
    self.move_key_turtle = self.create_publisher(Twist, '/cmd_vel', self.qos_profile)
    self.timer = self.create_timer(1, self.turtle_key_move)
    self.velocity = 0.0
    self.angular = 0.0

    self.latest_mp_key = None
    self.mediapipe_sub =self.create_subscription(String,'mediapipe_topic',self.mediapipe_cb,self.qos_profile)

  def mediapipe_cb(self,msg:String):
    self.latest_mp_key = (msg.data or "").strip().lower()[:1]
    # turtle_key_move()가 mediapipe 데이터를 참조할 방법이 없어.
    #최소로는 이렇게 저장해야 해:
    self.get_logger().info(f'mediapipe_cb{msg.data}')

  def turtle_key_move(self):
    msg = Twist()
    if self.latest_mp_key is not None:
      input_key = self.latest_mp_key
      self.latest_mp_key = None
    else:
      input_key = input('wasd 입력: ')[0].lower()

    print(input_key)
    if input_key in 'w'== msg.data:
       self.velocity += 0.1
    elif input_key in ['s','S']:
       self.velocity = 0.0
       self.angular = 0.0
    elif input_key in ['x','X']:
       self.velocity += -0.1
    elif input_key in ['a','A']:
       self.angular += 0.1
    elif input_key in ['d','D']:
       self.angular -= 0.1
    else:
      self.velocity = 0.0
      self.angular = 0.0

    msg.linear.x = self.velocity
    msg.linear.y = 0.0
    msg.linear.z = 0.0

    msg.angular.x = 0.0
    msg.angular.y = 0.0
    msg.angular.z = self.angular
    self.move_key_turtle.publish(msg)
    self.get_logger().info(f'Published mesage: {msg.linear}, {msg.angular}')

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

if __name__ == '__main':
  main()

