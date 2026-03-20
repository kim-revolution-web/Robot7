# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 's2.ui'
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
        Form.resize(727, 558)
        self.stackedWidget = QStackedWidget(Form)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(60, 30, 561, 401))
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.label = QLabel(self.page)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(100, 120, 67, 16))
        self.btn_2 = QPushButton(self.page)
        self.btn_2.setObjectName(u"btn_2")
        self.btn_2.setGeometry(QRect(310, 230, 95, 25))
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.btn_3 = QPushButton(self.page_2)
        self.btn_3.setObjectName(u"btn_3")
        self.btn_3.setGeometry(QRect(390, 300, 95, 25))
        self.label_2 = QLabel(self.page_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(160, 130, 141, 51))
        self.btn_back = QPushButton(self.page_2)
        self.btn_back.setObjectName(u"btn_back")
        self.btn_back.setGeometry(QRect(280, 90, 95, 25))
        self.stackedWidget.addWidget(self.page_2)

        self.retranslateUi(Form)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"first", None))
        self.btn_2.setText(QCoreApplication.translate("Form", u"\ub2e4\uc74c\ud398\uc774\uc9c0", None))
        self.btn_3.setText(QCoreApplication.translate("Form", u"PushButton", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.btn_back.setText(QCoreApplication.translate("Form", u"\ub3cc\uc544\uac00\uae30", None))
    # retranslateUi

