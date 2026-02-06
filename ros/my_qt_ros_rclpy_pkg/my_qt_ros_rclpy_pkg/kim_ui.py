# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'kim.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QWidget)
from .img import img_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1054, 868)
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(220, 130, 200, 200))
        self.label.setPixmap(QPixmap(u":/newPrefix/\uae40\ucc44\uc5f0.png"))
        self.label.setScaledContents(True)
        self.btn_right = QPushButton(Form)
        self.btn_right.setObjectName(u"btn_right")
        self.btn_right.setGeometry(QRect(420, 340, 200, 200))
        self.btn_right.setStyleSheet(u"border: none;\n"
"padding: 0px;\n"
"border-image: url(file:///home/robot/Desktop/961febbbfd4fa2e4.jpg);")
        icon = QIcon()
        icon.addFile(u"../../../../Desktop/1961febbbfd4fa2e4.jpg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_right.setIcon(icon)
        self.btn_right.setIconSize(QSize(16, 16))
        self.listWidget = QListWidget(Form)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(700, 30, 341, 471))
        self.btn_front = QPushButton(Form)
        self.btn_front.setObjectName(u"btn_front")
        self.btn_front.setGeometry(QRect(220, 130, 200, 200))
        self.btn_front.setStyleSheet(u"border: none;\n"
"padding: 0px;\n"
"border-image: url(file:///home/robot/Desktop/961febbbfd4fa2e4.jpg);")
        self.btn_front.setIcon(icon)
        self.btn_front.setIconSize(QSize(16, 16))
        self.btn_back = QPushButton(Form)
        self.btn_back.setObjectName(u"btn_back")
        self.btn_back.setGeometry(QRect(240, 530, 200, 200))
        self.btn_back.setStyleSheet(u"border: none;\n"
"padding: 0px;\n"
"border-image: url(file:///home/robot/Desktop/961febbbfd4fa2e4.jpg);")
        self.btn_back.setIcon(icon)
        self.btn_back.setIconSize(QSize(16, 16))
        self.btn_left = QPushButton(Form)
        self.btn_left.setObjectName(u"btn_left")
        self.btn_left.setGeometry(QRect(20, 330, 200, 200))
        self.btn_left.setStyleSheet(u"border: none;\n"
"padding: 0px;\n"
"border-image: url(file:///home/robot/Desktop/961febbbfd4fa2e4.jpg);")
        self.btn_left.setIcon(icon)
        self.btn_left.setIconSize(QSize(16, 16))
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(220, 540, 200, 200))
        self.label_2.setPixmap(QPixmap(u":/newPrefix/1961febbbfd4fa2e4.jpg"))
        self.label_2.setScaledContents(True)
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(420, 340, 200, 200))
        self.label_3.setPixmap(QPixmap(u":/newPrefix/401452_490340_4225.jpg"))
        self.label_3.setScaledContents(True)
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(20, 330, 200, 200))
        self.label_4.setPixmap(QPixmap(u":/newPrefix/humor_1609476_20250823150432_b8b00473c29481b4_poster.jpg"))
        self.label_4.setScaledContents(True)
        self.label_2.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.label.raise_()
        self.btn_left.raise_()
        self.btn_back.raise_()
        self.btn_right.raise_()
        self.btn_front.raise_()
        self.listWidget.raise_()

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText("")
        self.btn_right.setText(QCoreApplication.translate("Form", u"PushButton", None))
        self.btn_front.setText(QCoreApplication.translate("Form", u"PushButton", None))
        self.btn_back.setText(QCoreApplication.translate("Form", u"PushButton", None))
        self.btn_left.setText(QCoreApplication.translate("Form", u"PushButton", None))
        self.label_2.setText("")
        self.label_3.setText("")
        self.label_4.setText("")
    # retranslateUi

