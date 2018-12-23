# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Detail.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
class Ui_Detail_Dialog(object):
    def setupUi(self, Dialog, RuleDetail):
        # RuleDetail should be a dict wrapping the details of a rule.
        print(RuleDetail)
        Dialog.setObjectName("Dialog")
        Dialog.resize(741, 245)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(20, 30, 711, 141))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(7)
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
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(340, 210, 75, 23))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        self.parseRule(RuleDetail)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "规则类型"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "作用对象"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "逻辑操作"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "值"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "作用范围"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Dialog", "规则描述"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Dialog", "规则连接符"))
        self.pushButton.setText(_translate("Dialog", "关闭"))
    
    def parseRule(self, RuleDetail):
        _translate = QtCore.QCoreApplication.translate
        
        for i in range(len(RuleDetail['simpleRules'])):
            j = 0
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            item = QtWidgets.QTableWidgetItem('default')
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(i, j, item)
            j += 1
            item = QtWidgets.QTableWidgetItem(RuleDetail['simpleRules'][i]['subject'])
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(i, j, item)
            j += 1
            item = QtWidgets.QTableWidgetItem(RuleDetail['simpleRules'][i]['operation'])
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(i, j, item)
            j += 1
            item = QtWidgets.QTableWidgetItem(str(RuleDetail['simpleRules'][i]['val']))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(i, j, item)
            j += 1
            item = QtWidgets.QTableWidgetItem(RuleDetail['applyScope'])
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(i, j, item)
            j += 1
            item = QtWidgets.QTableWidgetItem(RuleDetail['description'])
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(i, j, item)
            j += 1
            if len(RuleDetail['operation']) == 1 or i == len(RuleDetail['simpleRules']) - 1:
                continue
            item = QtWidgets.QTableWidgetItem(RuleDetail['operation'][i+1])
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(i, j, item)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv) 
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Dialog()
    ui.setupUi(MainWindow)
    MainWindow.show()  
    sys.exit(app.exec_()) 