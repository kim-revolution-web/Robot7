# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'container1.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QStackedWidget, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(804, 587)
        self.stackedWidget = QStackedWidget(Form)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(110, 10, 631, 501))
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        self.label_2 = QLabel(self.page_1)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(250, 210, 67, 17))
        self.pushButton_2 = QPushButton(self.page_1)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(230, 270, 95, 25))
        self.stackedWidget.addWidget(self.page_1)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.label_3 = QLabel(self.page_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(240, 230, 67, 17))
        self.pushButton_3 = QPushButton(self.page_2)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(250, 290, 95, 25))
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.label_4 = QLabel(self.page_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(270, 180, 67, 17))
        self.pushButton_4 = QPushButton(self.page_3)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(270, 250, 95, 25))
        self.stackedWidget.addWidget(self.page_3)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.label = QLabel(self.page)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(150, 170, 67, 17))
        self.pushButton = QPushButton(self.page)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(160, 240, 95, 25))
        self.stackedWidget.addWidget(self.page)

        self.retranslateUi(Form)

        self.stackedWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"2page", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"PushButton2", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"3page", None))
        self.pushButton_3.setText(QCoreApplication.translate("Form", u"PushButton3", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"4page", None))
        self.pushButton_4.setText(QCoreApplication.translate("Form", u"PushButton4", None))
        self.label.setText(QCoreApplication.translate("Form", u"1page", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"PushButton1", None))
    # retranslateUi

