import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem,QStackedWidget
from PySide6.QtCore import QFile
# ui_test.py에서 Ui FORM을 import한다.
from container1_ui import Ui_Form

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Form()
        # setupUi 함수를 호출해 MainWindow에 있는 위젯을 배치한다.
        self.ui.setupUi(self)

        #setCuttentIndex(페이지번호)함수로 현재 페이지를 설정할 수 있습니다.
        self.ui.pushButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.pushButton_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.pushButton_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.pushButton_4.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
