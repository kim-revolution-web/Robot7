import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QRadioButton, QWidget
from PySide6.QtCore import QFile
from f1_ui import Ui_bnt_move_main

class FirstPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_bnt_move_main()
        self.ui.setupUi(self)


        self.ui.btn_1.clicked.connect(self.MoveMainPage)

    def MoveMainPage(self):
        self.parent().setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FirstPage()
    window.show()
    sys.exit(app.exec())
