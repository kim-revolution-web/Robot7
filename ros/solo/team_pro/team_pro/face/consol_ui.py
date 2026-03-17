# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'consol.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QLabel, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QStackedWidget,
    QTabWidget, QWidget)
import img2_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(775, 558)
        self.stackedWidget = QStackedWidget(Form)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(10, 10, 751, 521))
        self.stackedWidget.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.listWidget = QListWidget(self.page)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(10, 70, 151, 341))
        self.listWidget.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.groupBox_page = QGroupBox(self.page)
        self.groupBox_page.setObjectName(u"groupBox_page")
        self.groupBox_page.setGeometry(QRect(190, 430, 301, 51))
        self.label_page = QLabel(self.groupBox_page)
        self.label_page.setObjectName(u"label_page")
        self.label_page.setGeometry(QRect(110, 0, 81, 50))
        font = QFont()
        font.setPointSize(20)
        self.label_page.setFont(font)
        self.btn_pre = QPushButton(self.groupBox_page)
        self.btn_pre.setObjectName(u"btn_pre")
        self.btn_pre.setGeometry(QRect(0, 0, 110, 50))
        self.btn_next = QPushButton(self.groupBox_page)
        self.btn_next.setObjectName(u"btn_next")
        self.btn_next.setGeometry(QRect(190, 0, 110, 50))
        self.Face_listWidget = QListWidget(self.page)
        self.Face_listWidget.setObjectName(u"Face_listWidget")
        self.Face_listWidget.setGeometry(QRect(190, 40, 321, 361))
        self.battery_label = QLabel(self.page)
        self.battery_label.setObjectName(u"battery_label")
        self.battery_label.setGeometry(QRect(530, 30, 221, 31))
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.tabWidget = QTabWidget(self.page_2)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(80, 10, 511, 391))
        self.tabWidget.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.groupBox_page_2 = QGroupBox(self.page_2)
        self.groupBox_page_2.setObjectName(u"groupBox_page_2")
        self.groupBox_page_2.setGeometry(QRect(190, 450, 301, 51))
        self.label_page_2 = QLabel(self.groupBox_page_2)
        self.label_page_2.setObjectName(u"label_page_2")
        self.label_page_2.setGeometry(QRect(110, 0, 81, 50))
        self.label_page_2.setFont(font)
        self.btn_pre_2 = QPushButton(self.groupBox_page_2)
        self.btn_pre_2.setObjectName(u"btn_pre_2")
        self.btn_pre_2.setGeometry(QRect(0, 0, 110, 50))
        self.btn_next_2 = QPushButton(self.groupBox_page_2)
        self.btn_next_2.setObjectName(u"btn_next_2")
        self.btn_next_2.setGeometry(QRect(190, 0, 110, 50))
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.groupBox_page_3 = QGroupBox(self.page_3)
        self.groupBox_page_3.setObjectName(u"groupBox_page_3")
        self.groupBox_page_3.setGeometry(QRect(200, 420, 301, 51))
        self.label_page_3 = QLabel(self.groupBox_page_3)
        self.label_page_3.setObjectName(u"label_page_3")
        self.label_page_3.setGeometry(QRect(110, 0, 81, 50))
        self.label_page_3.setFont(font)
        self.btn_pre_3 = QPushButton(self.groupBox_page_3)
        self.btn_pre_3.setObjectName(u"btn_pre_3")
        self.btn_pre_3.setGeometry(QRect(0, 0, 110, 50))
        self.btn_next_3 = QPushButton(self.groupBox_page_3)
        self.btn_next_3.setObjectName(u"btn_next_3")
        self.btn_next_3.setGeometry(QRect(190, 0, 110, 50))
        self.groupBox_btns = QGroupBox(self.page_3)
        self.groupBox_btns.setObjectName(u"groupBox_btns")
        self.groupBox_btns.setGeometry(QRect(190, 30, 301, 331))
        self.groupBox_go = QGroupBox(self.groupBox_btns)
        self.groupBox_go.setObjectName(u"groupBox_go")
        self.groupBox_go.setGeometry(QRect(100, 20, 100, 100))
        self.label_go = QLabel(self.groupBox_go)
        self.label_go.setObjectName(u"label_go")
        self.label_go.setGeometry(QRect(0, 0, 100, 100))
        self.label_go.setPixmap(QPixmap(u":/newPrefix/arrow_up.jpg"))
        self.label_go.setScaledContents(True)
        self.btn_go = QPushButton(self.groupBox_go)
        self.btn_go.setObjectName(u"btn_go")
        self.btn_go.setGeometry(QRect(0, 0, 100, 100))
        self.btn_go.setStyleSheet(u"QPushButton {\n"
"  background-color: transparent;\n"
"  border: none;\n"
"  color: transparent;   /* \uae00\uc790\ub3c4 \uc548 \ubcf4\uc774\uac8c */\n"
"}")
        self.groupBox_stop = QGroupBox(self.groupBox_btns)
        self.groupBox_stop.setObjectName(u"groupBox_stop")
        self.groupBox_stop.setGeometry(QRect(100, 120, 100, 100))
        self.label_stop = QLabel(self.groupBox_stop)
        self.label_stop.setObjectName(u"label_stop")
        self.label_stop.setGeometry(QRect(0, 0, 100, 100))
        self.label_stop.setStyleSheet(u"")
        self.label_stop.setPixmap(QPixmap(u":/newPrefix/stop.jpg"))
        self.label_stop.setScaledContents(True)
        self.btn_stop = QPushButton(self.groupBox_stop)
        self.btn_stop.setObjectName(u"btn_stop")
        self.btn_stop.setGeometry(QRect(0, 0, 100, 100))
        self.btn_stop.setStyleSheet(u"QPushButton {\n"
"  background-color: transparent;\n"
"  border: none;\n"
"  color: transparent;   /* \uae00\uc790\ub3c4 \uc548 \ubcf4\uc774\uac8c */\n"
"}")
        self.groupBox_right = QGroupBox(self.groupBox_btns)
        self.groupBox_right.setObjectName(u"groupBox_right")
        self.groupBox_right.setGeometry(QRect(200, 120, 100, 100))
        self.label_right = QLabel(self.groupBox_right)
        self.label_right.setObjectName(u"label_right")
        self.label_right.setGeometry(QRect(0, 0, 100, 100))
        self.label_right.setPixmap(QPixmap(u":/newPrefix/arrow_right.jpg"))
        self.label_right.setScaledContents(True)
        self.btn_right = QPushButton(self.groupBox_right)
        self.btn_right.setObjectName(u"btn_right")
        self.btn_right.setGeometry(QRect(0, 0, 100, 100))
        self.btn_right.setStyleSheet(u"QPushButton {\n"
"  background-color: transparent;\n"
"  border: none;\n"
"  color: transparent;   /* \uae00\uc790\ub3c4 \uc548 \ubcf4\uc774\uac8c */\n"
"}")
        self.groupBox_left = QGroupBox(self.groupBox_btns)
        self.groupBox_left.setObjectName(u"groupBox_left")
        self.groupBox_left.setGeometry(QRect(0, 120, 100, 100))
        self.label_left = QLabel(self.groupBox_left)
        self.label_left.setObjectName(u"label_left")
        self.label_left.setGeometry(QRect(0, 0, 100, 100))
        self.label_left.setPixmap(QPixmap(u":/newPrefix/arrow_left.jpg"))
        self.label_left.setScaledContents(True)
        self.btn_left = QPushButton(self.groupBox_left)
        self.btn_left.setObjectName(u"btn_left")
        self.btn_left.setGeometry(QRect(0, 0, 100, 100))
        self.btn_left.setStyleSheet(u"QPushButton {\n"
"  background-color: transparent;\n"
"  border: none;\n"
"  color: transparent;   /* \uae00\uc790\ub3c4 \uc548 \ubcf4\uc774\uac8c */\n"
"}")
        self.groupBox_back = QGroupBox(self.groupBox_btns)
        self.groupBox_back.setObjectName(u"groupBox_back")
        self.groupBox_back.setGeometry(QRect(100, 230, 100, 100))
        self.label_back = QLabel(self.groupBox_back)
        self.label_back.setObjectName(u"label_back")
        self.label_back.setGeometry(QRect(0, 0, 100, 100))
        self.label_back.setPixmap(QPixmap(u":/newPrefix/arrow_down.jpg"))
        self.label_back.setScaledContents(True)
        self.btn_back = QPushButton(self.groupBox_back)
        self.btn_back.setObjectName(u"btn_back")
        self.btn_back.setGeometry(QRect(0, 0, 100, 100))
        self.btn_back.setStyleSheet(u"QPushButton {\n"
"  background-color: transparent;\n"
"  border: none;\n"
"  color: transparent;   /* \uae00\uc790\ub3c4 \uc548 \ubcf4\uc774\uac8c */\n"
"}")
        self.stackedWidget.addWidget(self.page_3)

        self.retranslateUi(Form)

        self.stackedWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox_page.setTitle("")
        self.label_page.setText(QCoreApplication.translate("Form", u"1page", None))
        self.btn_pre.setText(QCoreApplication.translate("Form", u" Previous page", None))
        self.btn_next.setText(QCoreApplication.translate("Form", u" Next page", None))
        self.battery_label.setText(QCoreApplication.translate("Form", u"\ubc30\ud130\ub9ac \uc794\ub7c9 :", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Form", u"Tab 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Form", u"Tab 2", None))
        self.groupBox_page_2.setTitle("")
        self.label_page_2.setText(QCoreApplication.translate("Form", u"2page", None))
        self.btn_pre_2.setText(QCoreApplication.translate("Form", u" Previous page", None))
        self.btn_next_2.setText(QCoreApplication.translate("Form", u" Next page", None))
        self.groupBox_page_3.setTitle("")
        self.label_page_3.setText(QCoreApplication.translate("Form", u"3page", None))
        self.btn_pre_3.setText(QCoreApplication.translate("Form", u" Previous page", None))
        self.btn_next_3.setText(QCoreApplication.translate("Form", u" Next page", None))
        self.groupBox_btns.setTitle(QCoreApplication.translate("Form", u"GroupBox", None))
        self.groupBox_go.setTitle("")
        self.label_go.setText("")
        self.btn_go.setText(QCoreApplication.translate("Form", u"go", None))
        self.groupBox_stop.setTitle("")
        self.label_stop.setText("")
        self.btn_stop.setText(QCoreApplication.translate("Form", u"stop", None))
        self.groupBox_right.setTitle("")
        self.label_right.setText("")
        self.btn_right.setText(QCoreApplication.translate("Form", u"right", None))
        self.groupBox_left.setTitle("")
        self.label_left.setText("")
        self.btn_left.setText(QCoreApplication.translate("Form", u"left", None))
        self.groupBox_back.setTitle("")
        self.label_back.setText("")
        self.btn_back.setText(QCoreApplication.translate("Form", u"down", None))
    # retranslateUi

