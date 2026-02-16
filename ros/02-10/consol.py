import sys
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from tb3_tsar_interfaces.msg import MyMsg

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer

from rclpy.qos import QoSProfile, QoSDurabilityPolicy, QoSHistoryPolicy, QoSReliabilityPolicy
from .consol_ui import Ui_Form
from rclpy.callback_groups import ReentrantCallbackGroup


class Tsar_Node(Node):
   def __init__(self):
    super().__init__('consol_move')

    self.declare_parameter('qos_depth', 10)
    qos_depth = self.get_parameter('qos_depth').value #현재값을 가져온다
    self.callback_group = ReentrantCallbackGroup()

    qos = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,#꼭 전달해라
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=qos_depth,
            durability=QoSDurabilityPolicy.VOLATILE)#과거는 잊고 현재 것만 준다

    self.pub = self.create_publisher(
            MyMsg,
            'ui_pub_sub',
            qos,
            callback_group=self.callback_group)

    # self.stop_service_clint = self.create_client(String, 'stop_service')
    # self.stop_clint = stop_service_clint.Request()

class MainWindow(QMainWindow):

    def __init__(self, tsar_node: Tsar_Node): #type이 함수니까
        super().__init__()
        self.tsar = tsar_node


        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # button clicked 이벤트 핸들러로 button_clicked 함수와 연결한다.
        self.ui.btn_go.clicked.connect(self.btn_go_Function)
        self.ui.btn_back.clicked.connect(self.btn_back_Function)
        self.ui.btn_right.clicked.connect(self.btn_right_Function)
        self.ui.btn_left.clicked.connect(self.btn_left_Function)
        self.ui.btn_stop.clicked.connect(self.btn_stop_Function)

        self.ui.btn_next.clicked.connect(lambda : self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.btn_pre.clicked.connect(lambda : self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.btn_next_2.clicked.connect(lambda : self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.btn_pre_2.clicked.connect(lambda : self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.btn_next_3.clicked.connect(lambda : self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.btn_pre_3.clicked.connect(lambda : self.ui.stackedWidget.setCurrentIndex(1))

        self.linear = 0.0
        self.angular = 0.0
        self.step = 0.2

    def publish_ui(self):
        msg = MyMsg()
        self.tsar.pub.publish(msg)
        self.tsar.get_logger().info(f"Published: linear={msg.linear}, angular={msg.angular}")
        self.ui.listWidget.addItem(f"{msg.linear:.2f}{msg.angular:.2f}")

    def btn_go_Function(self):
        self.linear += self.step
        self.angular = 0
        self.publish_ui()

    def btn_back_Function(self):
        self.linear -= self.step
        self.angular = 0
        self.publish_ui()

    def btn_left_Function(self):
        self.angular += self.step
        self.publish_ui()

    def btn_right_Function(self):
        self.angular -= self.step
        self.publish_ui()

    def btn_stop_Function(self):
        self.linear =0
        self.angular = 0
        self.publish_ui()



def main(args=None):
  rclpy.init(args=args)#ROS2 파이썬을 초기화.
  app = QApplication(sys.argv)#Qt 앱(이벤트 루프) 객체 생성.
  node = Tsar_Node()
  window = MainWindow(node)
  window.show()

  spin_timer = QTimer()
  spin_timer.timeout.connect(lambda: rclpy.spin_once(node,timeout_sec=0.0))#QTimer가 시간이 될 때마다 발생
  spin_timer.start(10)#10ms마다 timeout 신호 발생
  try:
    end=app.exec()   # Qt 이벤트 루프 실행 (여기가 메인)
  except KeyboardInterrupt:
    node.get_logger().info('Keyboard Interrupt (SIGINT)')
    end =0
  finally:
    node.destroy_node()
    rclpy.shutdown()
    sys.exit(end)


if __name__ == '__main__':
  main()
