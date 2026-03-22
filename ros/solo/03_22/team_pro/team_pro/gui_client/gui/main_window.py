from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QTimer


from .gui_ui import Ui_Form
from .media_player import FaceVideo #파일

#03/22
import cv2
from PySide6.QtGui import QImage, QPixmap


class MainWindow(QMainWindow):
    def __init__(self, GuiNode):
        super().__init__()
        self.gui_node = GuiNode

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.linear = 0.0
        self.angular = 0.0
        self.step = 0.01

        self.connect_buttons()
        self.connect_pages()

        self.ui.battery_label.setText("Battery: no data")
        self.battery_timer = QTimer(self)
        self.battery_timer.timeout.connect(self.update_battery_label)
        self.battery_timer.start(200)

        #media_player.py
        self.facevideo = FaceVideo(self, self.ui.face_widget)

        #03/22
        self.ui.camera_label.setText("Camera : no data")
        self.camera_timer = QTimer(self)
        self.camera_timer.timeout.connect(self.update_camera)
        self.camera_timer.start(33)   # 대략 30fps

    def connect_buttons(self):
        self.ui.btn_go.clicked.connect(self.btn_go_function)
        self.ui.btn_back.clicked.connect(self.btn_back_function)
        self.ui.btn_right.clicked.connect(self.btn_right_function)
        self.ui.btn_left.clicked.connect(self.btn_left_function)
        self.ui.btn_stop.clicked.connect(self.btn_stop_function)
        self.ui.btn_face.clicked.connect(self.publish_face)

    def connect_pages(self):
        self.ui.btn_next_0.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(1)
        )
        self.ui.btn_pre_0.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(3)
        )

        self.ui.btn_next_1.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(2)
        )
        self.ui.btn_pre_1.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(0)
        )

        self.ui.btn_next_2.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(3)
        )
        self.ui.btn_pre_2.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(1)
        )

        self.ui.btn_next_3.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(0)
        )
        self.ui.btn_pre_3.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(2)
        )

    def btn_go_function(self):
        self.linear += self.step
        self.angular = 0.0
        self.publish_ui()

    def btn_back_function(self):
        self.linear -= self.step
        self.angular = 0.0
        self.publish_ui()

    def btn_left_function(self):
        self.angular += self.step
        self.publish_ui()

    def btn_right_function(self):
        self.angular -= self.step
        self.publish_ui()

    def btn_stop_function(self):
        self.linear = 0.0
        self.angular = 0.0
        self.publish_ui()

    #gui_node.py
    def publish_ui(self):
        self.gui_node.publish_twist(self.linear, self.angular)
        self.ui.listWidget.addItem(
            f"linear:{self.linear:.2f}, angular:{self.angular:.2f}"
        )

    #gui_node.py
    def update_battery_label(self):
        self.ui.battery_label.setText(self.gui_node.battery_text())

    #gui_node.py
    def publish_face(self):
        text = self.ui.Face_lineEdit.text().strip().lower()
        if not text:
            return

        face_name = self.gui_node.publish_face_bundle(text)
        self.face_list(face_name)

    #media_player.py
    def face_list(self, text: str):
        self.ui.Face_listWidget.addItem(text)
        self.facevideo.play_face(text)

    #gui_node.py 03/22
    def update_camera(self):
        frame = self.gui_node.camera
        if frame is None:
            return

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #qt에 맞게 rgb변환
        h, w, ch = rgb.shape
        bytes_per_line = ch * w #이미지 한 줄(한 행)
        qimg = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)

        self.ui.camera_label.setPixmap(pixmap)
