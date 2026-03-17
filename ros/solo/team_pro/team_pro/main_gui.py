import sys
import rclpy
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

try:
    from .gui.main_window import MainWindow #파일
    from .ros.tsar_node import TsarNode #파일
except ImportError:
    from gui.main_window import MainWindow
    from team_pro.team_pro.ros.tsar_node import TsarNode


def main(args=None):
    rclpy.init(args=args)

    app = QApplication(sys.argv)
    node = TsarNode()
    window = MainWindow(node)
    window.show()

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
        if rclpy.ok():
            rclpy.shutdown()
        sys.exit(end)


if __name__ == '__main__':
    main()
