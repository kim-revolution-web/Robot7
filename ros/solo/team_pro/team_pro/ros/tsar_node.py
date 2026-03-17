from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import BatteryState
from rclpy.qos import (
    QoSProfile,
    QoSDurabilityPolicy,
    QoSHistoryPolicy,
    QoSReliabilityPolicy,
)
from rclpy.callback_groups import ReentrantCallbackGroup

class TsarNode(Node):
    def __init__(self):
        super().__init__('gui_controller')

        self.declare_parameter('qos_depth', 10)
        qos_depth = self.get_parameter('qos_depth').value

        self.callback_group = ReentrantCallbackGroup()

        qos = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=qos_depth,
            durability=QoSDurabilityPolicy.VOLATILE,
        )
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', qos)

        self.face_pub = self.create_publisher(String, '/face_cmd', qos)
        self.buzzer_pub = self.create_publisher(String, '/buzzer_cmd', qos)
        self.tail_pub = self.create_publisher(String, '/tail_cmd', qos)

        self.battery = None

        self.battery_sub = self.create_subscription(
            BatteryState,
            '/battery_state',
            self.cb_battery,
            qos,
        )
    def cb_battery(self, msg: BatteryState):
        self.battery = msg
        self.get_logger().info(
            f"Battery recv: voltage={msg.voltage}, percentage={msg.percentage}"
        )
    def publish_twist(self, linear: float, angular: float):
        msg = Twist()
        msg.linear.x = float(linear)
        msg.angular.z = float(angular)

        self.cmd_pub.publish(msg)
        self.get_logger().info(
            f"Published cmd_vel: linear.x={msg.linear.x}, angular.z={msg.angular.z}"
        )
    def publish_face_bundle(self, text: str) -> str:
        text = text.strip().lower()

        if text == "angry":
            face_cmd = "angry"
            tail_cmd = "angry"
            buzzer_cmd = "warning"

        elif text == "heart":
            face_cmd = "heart"
            tail_cmd = "friendly"
            buzzer_cmd = "happy"

        elif text == "neutral":
            face_cmd = "neutral"
            tail_cmd = "normal"
            buzzer_cmd = "stop"

        elif text == "cry":
            face_cmd = "cry"
            tail_cmd = "stop"
            buzzer_cmd = "danger"

        else :
            face_cmd = text
            tail_cmd = text
            buzzer_cmd = "stop"

        face_msg = String()
        face_msg.data = face_cmd

        tail_msg = String()
        tail_msg.data = tail_cmd

        buzzer_msg = String()
        buzzer_msg.data = buzzer_cmd

        self.face_pub.publish(face_msg)
        self.tail_pub.publish(tail_msg)
        self.buzzer_pub.publish(buzzer_msg)

        self.get_logger().info(
            f"Published face={face_cmd}, tail={tail_cmd}, buzzer={buzzer_cmd}"
        )
        return face_cmd

    def battery_text(self) -> str:
        if self.battery is None:
            return "Battery: no data"

        battery = self.battery

        if battery.percentage >= 0.0:
            percent = battery.percentage
            return f"Battery: {percent:.2f}% ({battery.voltage:.2f}V)"

        return f"Battery: {battery.voltage:.2f}V"
