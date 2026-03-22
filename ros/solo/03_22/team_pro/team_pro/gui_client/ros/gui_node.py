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
# from rclpy.callback_groups import ReentrantCallbackGroup

#추가 03/18
from sensor_msgs.msg import Image
from cv_bridge import CvBridge



class GuiNode(Node):
    def __init__(self):
        super().__init__('gui_node')

        self.declare_parameter('qos_depth', 10)
        qos_depth = self.get_parameter('qos_depth').value

        qos = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=qos_depth,
            durability=QoSDurabilityPolicy.VOLATILE,
        )
        #pub
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', qos)
        self.face_pub = self.create_publisher(String, '/face_cmd', qos)
        self.buzzer_pub = self.create_publisher(String, '/buzzer_cmd', qos)
        self.tail_pub = self.create_publisher(String, '/tail_cmd', qos)

        self.battery = None
        self.bridge = CvBridge()
        self.camera= None

        #sub
        self.battery_sub = self.create_subscription(BatteryState,'/battery_state',self.cb_battery,qos)
        self.camera_sub = self.create_subscription(Image,"/image_raw",self.cb_camera,qos)

    #main_window.py에서 쓰지만 값을 바로 pub 해줘서 return을 쓰지 않음 이동
    def publish_twist(self, linear: float, angular: float):
        msg = Twist()
        msg.linear.x = float(linear)
        msg.angular.z = float(angular)

        self.cmd_pub.publish(msg)
        self.get_logger().info(
            f"Published cmd_vel: linear.x={msg.linear.x}, angular.z={msg.angular.z}"
        )

    #main_window.py
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

    def cb_battery(self, msg: BatteryState):
        self.battery = msg
        self.get_logger().info(
            f"Battery recv: voltage={msg.voltage}, percentage={msg.percentage}"
        )

    #03/22
    def cb_camera(self, msg : Image):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        self.camera = frame


    #main_window.py
    def battery_text(self) -> str:
        if self.battery is None:
            return "Battery: no data"
        #init 변수
        battery = self.battery

        if battery.percentage >= 0.0:
            percent = battery.percentage
            return f"Battery: {percent:.2f}% ({battery.voltage:.2f}V)"

        return f"Battery: {battery.voltage:.2f}V"
