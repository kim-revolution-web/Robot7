import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QRadioButton, QWidget
from PySide6.QtCore import QFile
from s2_ui import Ui_Form

class SecondPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.btn_2.clicked.connect(self.btn_moveNextpage_clicked)
        self.ui.btn_3.clicked.connect(self.btn_movePreviouspage_clicked)
        self.ui.btn_back.clicked.connect(lambda : self.parent().setCurrentIndex(0))


    def btn_moveNextpage_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def btn_movePreviouspage_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SecondPage()
    window.show()
    sys.exit(app.exec())
