import sys
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from geometry_msgs.msg import Twist

from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import QTimer

# from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
# from PySide6.QtCore import QFile, QThread, Signal, Slot
# from rclpy.executors import MultiThreadedExecutor

from .kim_ui import Ui_Form

class kim_Move_turtle(Node, QWidget):
    def __init__(self):
        Node.__init__(self, 'move_turtle')
        QWidget.__init__(self)

        self.qos_profile = QoSProfile(depth=10) #이거 깊이야?
        self.pub = self.create_publisher(Twist, 'turtle1/cmd_vel', self.qos_profile)# cmd_vel로 속도명령 보내는 송신기

        self.velocity = 0.5

        self.ui = Ui_Form() #ui에 필요
        self.ui.setupUi(self) ##ui가져오기

        self.ui.btn_front.clicked.connect(self.btn_frontpb)
        self.ui.btn_left.clicked.connect(self.btn_leftpb)
        self.ui.btn_right.clicked.connect(self.btn_rightpb)
        self.ui.btn_back.clicked.connect(self.btn_backpb)

    def btn_frontpb(self):
        msg = Twist() #속도 명령 메시지 1개를 새로 만든다
        msg.linear.x = float(self.velocity)
        msg.angular.z = 0.0
        self.pub.publish(msg) #turtlesim이 이 메시지를 받아서 움직임.
        self.get_logger().info(f'btn_frontpb: linear.x= {msg.linear.x}') #로고 띄워주기


    def btn_leftpb(self):
        msg = Twist() #속도 명령 메시지 1개를 새로 만든다
        msg.linear.x = float(self.velocity)
        msg.angular.z = float(self.velocity)
        self.pub.publish(msg) #turtlesim이 이 메시지를 받아서 움직임.
        self.get_logger().info(f'btn_leftpb: linear.x,linear.y= {msg.linear.x,msg.linear.x}') #로고 띄워주기

    def btn_rightpb(self):
        msg = Twist() #속도 명령 메시지 1개를 새로 만든다
        msg.linear.x = float(self.velocity)
        msg.angular.z = -float(self.velocity)
        self.pub.publish(msg) #turtlesim이 이 메시지를 받아서 움직임.
        self.get_logger().info(f'btn_rightpb: linear.x,linear.y= {msg.linear.x,msg.linear.x}') #로고 띄워주기

    def btn_backpb(self):
        msg = Twist() #속도 명령 메시지 1개를 새로 만든다
        msg.linear.x = -float(self.velocity)
        msg.angular.z = 0.0
        self.pub.publish(msg) #turtlesim이 이 메시지를 받아서 움직임.
        self.get_logger().info(f'btn_backpb: linear.x= {msg.linear.x}') #로고 띄워주기


def main(args=None):
    rclpy.init(args=args) #args 가져오기

    app = QApplication(sys.argv) #QApplication 객체가 반드시 1개 있어야 GUI가 돌아가.
    win = kim_Move_turtle() #클래스 객체 생성
    win.show()

    timer = QTimer()
    timer.timeout.connect(lambda: rclpy.spin_once(win, timeout_sec=0.001)) #ROS 콜백(타이머/구독/서비스 응답 등)을 Qt 이벤트루프랑 같이 돌리기 위한 트릭
    timer.start(50) #50ms(0.05초)마다 timeout 발생

    ret = 0
    try:
     ret = app.exec() #Qt 이벤트 루프 시작
    except KeyboardInterrupt:#ctral+c눌리면 종료
     pass
    finally:
     win.destroy_node() #함수 node 종료
     rclpy.shutdown()
     sys.exit(ret)

    #----------------------------
#     class HelloworldSubscriber(Node):

#     def __init__(self):
#         super().__init__('Helloworld_subscriber')
#         qos_profile = QoSProfile(depth=10)
#         self.helloworld_subscriber = self.create_subscription(
#             String,
#             'helloworld',
#             self.subscribe_topic_message,
#             qos_profile)

#     def subscribe_topic_message(self, msg):
#         self.get_logger().info('Received message: {0}'.format(msg.data))

# def main(args=None):
#     rclpy.init(args=args)
#     node = HelloworldSubscriber()
#     try:
#         rclpy.spin(node)
#     except KeyboardInterrupt:
#         node.get_logger().info('Keyboard Interrupt (SIGINT)')
#     finally:
#         node.destroy_node()
#         rclpy.shutdown()





if __name__ == '__main__':
    main()
