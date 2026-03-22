import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from sensor_msgs.msg import CompressedImage
from rclpy.qos import (
    QoSProfile,
    QoSDurabilityPolicy,
    QoSHistoryPolicy,
    QoSReliabilityPolicy,
)
import cv2
import numpy as np

from ..vision.detector import VisionDetector

class ImageNode(Node):
    def __init__(self):
        super().__init__('image_node')

        self.declare_parameter('qos_depth', 10)
        qos_depth = self.get_parameter('qos_depth').value

        qos = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=qos_depth,
            durability=QoSDurabilityPolicy.VOLATILE,
        )

        self.detector = VisionDetector()

        self.image_sub = self.create_subscription(
            CompressedImage,
            "/camera/image/compressed",
            self.image_callback,
            qos
        )

        self.img_result_pub = self.create_publisher(
            String,
            "/image_result",
            qos
        )

    def image_callback(self, msg: CompressedImage):
        np_arr = np.frombuffer(msg.data, np.uint8)
        #msg.data 바이트를
        #np.uint8 타입의 numpy 배열로 해석
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        #진짜 이미지(BGR frame) 로 복원하는 거야.
        if frame is None:
            self.get_logger().warning("frame decode failed")
            return

        result = self.detector.detect(frame)

        out_msg = String()
        out_msg.data = result
        self.img_result_pub.publish(out_msg)
