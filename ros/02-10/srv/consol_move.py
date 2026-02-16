import sys
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_srvs.srv import Trigger  # ✅ 서비스 타입

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer

from rclpy.qos import QoSProfile, QoSDurabilityPolicy, QoSHistoryPolicy, QoSReliabilityPolicy
from .consol_ui import Ui_Form
from rclpy.callback_groups import ReentrantCallbackGroup


class Tsar_Node(Node):
    def __init__(self):
        super().__init__('consol_move')

        self.declare_parameter('qos_depth', 10)
        qos_depth = self.get_parameter('qos_depth').value
        self.callback_group = ReentrantCallbackGroup()

        qos = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=qos_depth,
            durability=QoSDurabilityPolicy.VOLATILE
        )

        self.pub = self.create_publisher(
            String, 'ui_pub_sub', qos, callback_group=self.callback_group
        )

        # ✅ STOP 서비스 클라이언트
        self.stop_client = self.create_client(
            Trigger, 'stop_service', callback_group=self.callback_group
        )

    def call_stop_service(self):
        if not self.stop_client.service_is_ready():
            self.get_logger().warning("stop_service not ready yet.")
            return None
        req = Trigger.Request()
        future = self.stop_client.call_async(req)
        return future


class MainWindow(QMainWindow):
    def __init__(self, tsar_node: Tsar_Node):
        super().__init__()
        self.tsar = tsar_node

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.btn_go.clicked.connect(self.btn_go_Function)
        self.ui.btn_back.clicked.connect(self.btn_back_Function)
        self.ui.btn_right.clicked.connect(self.btn_right_Function)
        self.ui.btn_left.clicked.connect(self.btn_left_Function)
        self.ui.btn_stop.clicked.connect(self.btn_stop_Function)

        self.ui.btn_next.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.btn_pre.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.btn_next_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.btn_pre_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.btn_next_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.btn_pre_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))

        self.linear = 0.0
        self.angular = 0.0
        self.step = 0.2

    def publish_ui(self):
        msg = String()
        msg.data = f"{self.linear} {self.angular}"
        self.tsar.pub.publish(msg)
        self.tsar.get_logger().info(f"Published ui_pub_sub: {msg.data}")
        self.ui.listWidget.addItem(msg.data)

    def btn_go_Function(self):
        self.linear += self.step
        self.angular = 0.0
        self.publish_ui()

    def btn_back_Function(self):
        self.linear -= self.step
        self.angular = 0.0
        self.publish_ui()

    def btn_left_Function(self):
        self.angular += self.step
        self.publish_ui()

    def btn_right_Function(self):
        self.angular -= self.step
        self.publish_ui()

    # ✅ STOP: 토픽도 0으로 보내고 + 서비스로 "정지 확인"까지 받기
    def btn_stop_Function(self):
        self.linear = 0.0
        self.angular = 0.0
        self.publish_ui()  # 토픽으로도 0 0 보내기 (즉시성/호환성)

        future = self.tsar.call_stop_service()
        if future is None:
            self.ui.listWidget.addItem("STOP service not ready (only topic stop sent)")
            return

        # future 완료 시 결과 처리
        future.add_done_callback(self.on_stop_done)

    def on_stop_done(self, future):
        try:
            res = future.result()
            self.tsar.get_logger().info(f"STOP service response: success={res.success}, msg='{res.message}'")
            self.ui.listWidget.addItem(f"[STOP srv] {res.success} / {res.message}")
        except Exception as e:
            self.tsar.get_logger().error(f"STOP service call failed: {e}")
            self.ui.listWidget.addItem(f"[STOP srv] FAILED: {e}")


def main(args=None):
    rclpy.init(args=args)
    app = QApplication(sys.argv)

    node = Tsar_Node()
    window = MainWindow(node)
    window.show()

    # 서비스 서버 뜰 시간 조금 주는 느낌(필수는 아님)
    # node.stop_client.wait_for_service(timeout_sec=1.0)

    spin_timer = QTimer()
    spin_timer.timeout.connect(lambda: rclpy.spin_once(node, timeout_sec=0.0))
    spin_timer.start(10)

    try:
        end = app.exec()
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt (SIGINT)')
        end = 0
    finally:
        node.destroy_node()
        rclpy.shutdown()
        sys.exit(end)


if __name__ == '__main__':
    main()
