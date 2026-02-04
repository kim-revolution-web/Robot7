import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from PySide6.QtCore import QFile
# ui_test.py에서 Ui MainWindow를 import한다.
from listWidget_ui import Ui_Form



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Form()
        # setupUi 함수를 호출해 MainWindow에 있는 위젯을 배치한다.
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.button1Function)
        #0page
        self.ui.next_page.clicked.connect(lambda : self.ui.stackedWidget.setCurrentIndex(1))
        #self.ui.previous_page.clicked.connect(lambda : self.ui.stackedWidget.setCurrentIndex(2))
        #1page
        self.ui.next_page_2.clicked.connect(lambda : self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.previous_page_2.clicked.connect(lambda : self.ui.stackedWidget.setCurrentIndex(0))
        #2page
        #self.ui.next_page_3.clicked.connect(lambda : self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.previous_page_3.clicked.connect(lambda : self.ui.stackedWidget.setCurrentIndex(1))

#버튼 눌리면 리스트에 라인에 있는게 들어가고 라인은 클리어
    def button1Function(self) :
        text =self.ui.lineEdit.text().strip() #strip 공백제거
        self.ui.listWidget.addItem(text)
        self.ui.lineEdit.clear()

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
