from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QTimer

try:
    from .mygui_ui import Ui_Form
    from .media_player import FaceVideoPlayer #파일
except ImportError:
    from gui_ui import Ui_Form
    from media_player import FaceVideoPlayer


class MainWindow(QMainWindow):
    def __init__(self, tsar_node):
        super().__init__()
        self.tsar = tsar_node

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.linear = 0.0
        self.angular = 0.0
        self.step = 0.01

        self.video_player = FaceVideoPlayer(self, self.ui.face_widget) #media_player.py

        self.connect_buttons()
        self.connect_pages()

        self.ui.battery_label.setText("Battery: no data")
        self.battery_timer = QTimer(self)
        self.battery_timer.timeout.connect(self.update_battery_label)
        self.battery_timer.start(200)

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

    def publish_ui(self):
        self.tsar.publish_twist(self.linear, self.angular)
        self.ui.listWidget.addItem(
            f"linear:{self.linear:.2f}, angular:{self.angular:.2f}"
        )

    def publish_face(self):
        text = self.ui.Face_lineEdit.text().strip().lower()
        if not text:
            return

        face_name = self.tsar.publish_face_bundle(text)
        self.face_list(face_name)

    def face_list(self, text: str):
        self.ui.Face_listWidget.addItem(text)
        self.video_player.play_face(text)

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

    def update_battery_label(self):
        self.ui.battery_label.setText(self.tsar.battery_text())
