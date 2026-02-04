# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'container.ui'
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
    QTabWidget, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(695, 533)
        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(60, 30, 461, 401))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.pushButton_1 = QPushButton(self.tab)
        self.pushButton_1.setObjectName(u"pushButton_1")
        self.pushButton_1.setGeometry(QRect(60, 190, 95, 25))
        self.label_1 = QLabel(self.tab)
        self.label_1.setObjectName(u"label_1")
        self.label_1.setGeometry(QRect(40, 30, 191, 111))
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.pushButton_2 = QPushButton(self.tab_2)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(170, 210, 95, 25))
        self.label_2 = QLabel(self.tab_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(150, 90, 191, 111))
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.label_3 = QLabel(self.tab_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(50, 30, 191, 111))
        self.pushButton_3 = QPushButton(self.tab_3)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(70, 150, 95, 25))
        self.tabWidget.addTab(self.tab_3, "")

        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
#if QT_CONFIG(tooltip)
        self.tabWidget.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Tab3</p><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_1.setText(QCoreApplication.translate("Form", u"PushButton1", None))
        self.label_1.setText(QCoreApplication.translate("Form", u"PushButton1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Form", u"Tab 1", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"PushButton2", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"2page", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Form", u"Tab 2", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"3page", None))
        self.pushButton_3.setText(QCoreApplication.translate("Form", u"PushButton3", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Form", u"\ucabd", None))
    # retranslateUi

