import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from id_pd_ui import Ui_MainWindow
from loge_ui import Ui_logeWindow

class OtherWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_logeWindow()
        self.ui.setupUi(self)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        # setupUi 함수를 호출해 MainWindow에 있는 위젯을 배치한다.
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.button1Function)
        self.other_window = None  # 참조 유지용

    def button1Function(self):
        self.other=Ui_logeWindow()
        self.other.show()





if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec)

