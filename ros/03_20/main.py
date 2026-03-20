import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QRadioButton, QWidget, QStackedWidget
from PySide6.QtCore import QFile
from main_ui import Ui_Form

from s2main import SecondPage
from firstPageMain import FirstPage

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(lambda : widget.setCurrentIndex(1))
        self.ui.pushButton_2.clicked.connect(lambda : widget.setCurrentIndex(2))

    # def MoveFirstPage(self):
    #     widget.setCurrentIndex(1)

    # def MoveSecondPage(self):
    #     widget.setCurrentIndex(2)

if __name__ == "__main__":
      app = QApplication(sys.argv)
      window = MainWindow()
      firstPage = FirstPage()
      secondPage = SecondPage()
      widget = QStackedWidget()
      widget.addWidget(window)
      widget.addWidget(firstPage)
      widget.addWidget(secondPage)

      widget.setFixedHeight(400)
      widget.setFixedWidth(600)

      widget.show()
      sys.exit(app.exec())
