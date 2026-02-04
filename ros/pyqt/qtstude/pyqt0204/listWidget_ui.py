# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'listWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QStackedWidget,
    QTabWidget, QWidget)
import img_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(848, 730)
        self.stackedWidget = QStackedWidget(Form)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(20, 20, 731, 621))
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.listWidget = QListWidget(self.page)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(50, 10, 341, 281))
        self.lineEdit = QLineEdit(self.page)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(50, 350, 431, 81))
        self.pushButton = QPushButton(self.page)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(500, 350, 191, 81))
        self.label = QLabel(self.page)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(310, 590, 67, 17))
        self.next_page = QPushButton(self.page)
        self.next_page.setObjectName(u"next_page")
        self.next_page.setGeometry(QRect(340, 530, 101, 31))
        self.previous_page = QPushButton(self.page)
        self.previous_page.setObjectName(u"previous_page")
        self.previous_page.setGeometry(QRect(174, 534, 121, 31))
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.label_2 = QLabel(self.page_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(360, 590, 67, 17))
        self.previous_page_2 = QPushButton(self.page_2)
        self.previous_page_2.setObjectName(u"previous_page_2")
        self.previous_page_2.setGeometry(QRect(230, 540, 121, 31))
        self.next_page_2 = QPushButton(self.page_2)
        self.next_page_2.setObjectName(u"next_page_2")
        self.next_page_2.setGeometry(QRect(396, 536, 101, 31))
        self.label_4 = QLabel(self.page_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(100, 530, 67, 17))
        self.tabWidget = QTabWidget(self.page_2)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(10, 20, 671, 471))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.label_5 = QLabel(self.tab)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(10, 10, 291, 401))
        self.label_5.setPixmap(QPixmap(u":/newPrefix/14205317bc35bf89d2e67af2db323788557bac33.png"))
        self.label_5.setScaledContents(True)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.label_3 = QLabel(self.page_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(350, 580, 67, 17))
        self.previous_page_3 = QPushButton(self.page_3)
        self.previous_page_3.setObjectName(u"previous_page_3")
        self.previous_page_3.setGeometry(QRect(240, 530, 121, 31))
        self.next_page_3 = QPushButton(self.page_3)
        self.next_page_3.setObjectName(u"next_page_3")
        self.next_page_3.setGeometry(QRect(406, 526, 101, 31))
        self.stackedWidget.addWidget(self.page_3)

        self.retranslateUi(Form)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lineEdit.setText("")
        self.pushButton.setText(QCoreApplication.translate("Form", u"PushButton", None))
        self.label.setText(QCoreApplication.translate("Form", u"1/3", None))
        self.next_page.setText(QCoreApplication.translate("Form", u"next page", None))
        self.previous_page.setText(QCoreApplication.translate("Form", u"previous page", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"2/3", None))
        self.previous_page_2.setText(QCoreApplication.translate("Form", u"previous page", None))
        self.next_page_2.setText(QCoreApplication.translate("Form", u"next page", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.label_5.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Form", u"Tab 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Form", u"Tab 2", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"3/3", None))
        self.previous_page_3.setText(QCoreApplication.translate("Form", u"previous page", None))
        self.next_page_3.setText(QCoreApplication.translate("Form", u"next page", None))
    # retranslateUi

