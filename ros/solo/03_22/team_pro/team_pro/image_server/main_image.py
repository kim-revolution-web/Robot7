import rclpy
from .ros.image_node import ImageNode

def main(args=None):
    rclpy.init(args=args)
    node = ImageNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
  main()
