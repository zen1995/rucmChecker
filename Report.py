# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Report.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Report_Dialog(object):
    def setupUi(self, Dialog, reporter):
        Dialog.setObjectName("Dialog")
        Dialog.resize(826, 435)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(30, 20, 771, 351))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(730, 390, 75, 23))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "违规编号"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "违规用例"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "违规句段"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "违反规则"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "规则描述"))
        self.pushButton.setText(_translate("Dialog", "关闭"))

