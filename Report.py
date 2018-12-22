# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Report.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

import reporter
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import PyQt5
import sys
from PyQt5.QtCore import QCoreApplication
class Ui_Report_Dialog(object):
    def setupUi(self, Dialog):
        self.Dialog = Dialog

        Dialog.setObjectName("Dialog")
        Dialog.resize(826, 435)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(30, 20, 771, 351))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        # item = QtWidgets.QTableWidgetItem()
        # self.tableWidget.setHorizontalHeaderItem(3, item)
        # item = QtWidgets.QTableWidgetItem()
        # self.tableWidget.setHorizontalHeaderItem(4, item)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(730, 390, 75, 23))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.setVals()
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "规则描述"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "违规用例"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "违规句段"))
        item = self.tableWidget.horizontalHeaderItem(3)
        # item.setText(_translate("Dialog", "违反规则"))
        # item = self.tableWidget.horizontalHeaderItem(4)
        # item.setText(_translate("Dialog", "规则描述"))
        self.pushButton.setText(_translate("Dialog", "关闭"))
        self.pushButton.clicked.connect(self.Dialog.close)
    def setVals(self):
        # newItem = QTableWidgetItem('张三')
        # self.tableWidget.setItem(0, 0, newItem)
        self.tableWidget.setRowCount(len(reporter.Reporter.errors))

        for i in range(3):
            self.tableWidget.setColumnWidth(i,250)
        for i,e in enumerate(reporter.Reporter.errors):
            self.tableWidget.setItem(i,0,QTableWidgetItem(e.rulename))
            self.tableWidget.setItem(i,1,QTableWidgetItem(e.usecasename))
            self.tableWidget.setItem(i,2,QTableWidgetItem(e.sentence))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    reporter.Reporter.reportError('rule1', 'usecase1', 'I am kind')
    reporter.Reporter.reportError('rule2', 'usecase2', 'I am dog')
    reporter.Reporter.reportError('rule3', 'usecase3', 'I am cat')
    reporter.Reporter.reportError('rule4', 'usecase4', 'I am monkey')
    mainWindow = Ui_Report_Dialog()
    window = PyQt5.QtWidgets.QMainWindow()
    mainWindow.setupUi(window)

    window.show()
    print(app.exec_())




