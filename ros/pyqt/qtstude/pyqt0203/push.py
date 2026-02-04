import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from pushtest_ui import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        # setupUi 함수를 호출해 MainWindow에 있는 위젯을 배치한다.
        self.ui.setupUi(self)

        # button clicked 이벤트 핸들러로 button_clicked 함수와 연결한다.

        self.ui.pushButton1.setText("btn1")
        self.ui.pushButton1.clicked.connect(self.button1Function)
        self.ui.pushButton2.clicked.connect(self.button2Function)
        self.ui.pushButton2.setText("우승자는?")
        self.ui.lineEdit.returnPressed.connect(self.lineEditReturnPressed)
        self.ui.lineEdit_2.textChanged.connect(self.lineEditTextChanged)
     #-------------------------------------------------------------
        self.ui.radioButton.clicked.connect(self.radioBtn1)
        self.ui.radioButton.setText("들기름 조림")
        self.ui.radioButton_2.clicked.connect(self.radioBtn2)
        self.ui.radioButton_2.setText("고추장 조림")
        self.ui.radioButton_3.clicked.connect(self.radioBtn3)
        self.ui.radioButton_4.clicked.connect(self.radioBtn4)
        self.ui.radioButton_5.clicked.connect(self.radioBtn5)
        self.ui.radioButton_6.clicked.connect(self.radioBtn6)
        self.ui.radioButton_7.clicked.connect(self.radioBtn7)

        self.ui.checkBox.toggled.connect(self.checktog)
        self.ui.checkBox_2.checkStateChanged.connect(self.checkclicked)
#------------------------------------------------------------------------
        self.ui.comboBox.addItems(["들조림","간장조림","조림핑"])
        self.items =["나야","너야","누구야","뭐야"]
        self.ui.comboBox_2.addItems(self.items)

        self.ui.comboBox.currentTextChanged.connect(self.combotext)
        self.ui.comboBox_2.activated.connect(self.comboactiv)
#--------------------------------------------------------------------------------

        self.ui.listWidget.addItem("들기름 라떼")
        self.ui.listWidget.addItem("참기름 라떼")
        self.ui.listWidget.addItem("깨기름 라떼")

        self.ui.listWidget.currentTextChanged.connect(self.listwidget)
        self.ui.listWidget.currentItem.connect(self.fill_list_from_combo())

    def fill_list_from_combo(self):
     self.ui.listWidget.clear()
     items = [self.ui.comboBox.itemText(i) for i in range(self.ui.comboBox.count())]
     self.ui.listWidget.addItems(items)

    def listwidget(self, text):
        self.ui.label_6.setText(text)

    def combotext(self,text):
        print(text)

    def comboactiv(self,idx):
        print(self.ui.comboBox_2.itemText(idx))


    def checkclicked(self):
        if self.ui.checkBox_2.isChecked():
            print(f"{self.ui.checkBox_2.text()}check2")
        else:
            print(f"{self.ui.checkBox_2.text()}no check2")

    def checktog(self,checked):
        if checked:
            print(f"{self.ui.checkBox.text()}check")
        else:
            print(f"{self.ui.checkBox.text()}no check")

    def radioBtn1(self):
        self.ui.label_5.setText(self.ui.radioButton.text())
    def radioBtn2(self):
        self.ui.label_5.setText(self.ui.radioButton_2.text())
    def radioBtn3(self):
        self.ui.label_5.setText(self.ui.radioButton_3.text())
    def radioBtn4(self):
        self.ui.label_5.setText(self.ui.radioButton_4.text())
    def radioBtn5(self):
        self.ui.label_5.setText(self.ui.radioButton_5.text())
    def radioBtn6(self):
        self.ui.label_6.setText(self.ui.radioButton_6.text())
    def radioBtn7(self):
        self.ui.label_6.setText(self.ui.radioButton_7.text())

    def lineEditReturnPressed(self):
        self.ui.lineEdit.setText(self.ui.lineEdit.text())
        self.ui.label_3.setText("ID")
    def lineEditTextChanged(self):
        self.ui.lineEdit_2.setText(self.ui.lineEdit_2.text()) #
        self.ui.label_4.setText("PD")



    #btn_1이 눌리면 작동할 함수
    def button1Function(self) :

        self.ui.pushButton1.text()
        print("btn_1 Clicked")
        self.ui.label.setText("김채연")

    #btn_2가 눌리면 작동할 함수
    def button2Function(self) :

        self.ui.pushButton2.text()
        print("btn_2 Clicked")
        self.ui.pushButton2.setText("최강록셰프")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
