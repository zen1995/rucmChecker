# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Detail.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import QApplication, QWidget,QToolTip,QPushButton
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtCore import QCoreApplication

class Ui_Detail_Dialog(object):
    def setupUi(self, Dialog, content):
        self.content = content
        Dialog.setObjectName("Dialog")
        Dialog.resize(741, 245)
        # self.pushButton = QtWidgets.QPushButton(Dialog)
        # self.pushButton.setGeometry(QtCore.QRect(330, 210, 75, 23))
        # self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(30, 20, 681, 181))
        self.textEdit.setObjectName("textEdit")

        self.retranslateUi(Dialog)
        # self.pushButton.clicked.connect(Dialog.quit)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        # self.pushButton.setText(_translate("Dialog", "关闭"))

        self.textEdit.setPlainText(str(self.content))

