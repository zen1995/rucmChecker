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
import copy
from PyQt5.QtCore import QCoreApplication
import rucmElement
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

        self.export_txt = QtWidgets.QPushButton(Dialog)
        self.export_txt.setGeometry(QtCore.QRect(630, 390, 75, 23))
        self.export_txt.setObjectName("export_txt")

        self.export_html = QtWidgets.QPushButton(Dialog)
        self.export_html.setGeometry(QtCore.QRect(530, 390, 75, 23))
        self.export_html.setObjectName("export_html")

        self.export_pdf = QtWidgets.QPushButton(Dialog)
        self.export_pdf.setGeometry(QtCore.QRect(430, 390, 75, 23))
        self.export_pdf.setObjectName("export_pdf")

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

        self.export_txt.setText("导出txt报告")
        self.export_txt.clicked.connect(self.export_txt_)
        self.export_html.setText("导出html报告")
        self.export_html.clicked.connect(lambda : (reporter.Reporter.to_html(QtWidgets.QFileDialog.getSaveFileName(self.Dialog,"输出路径",".")[0]),
        QMessageBox.information(self.Dialog, "message", "导出报告到完成")

                                                   ))
        self.export_pdf.setText("导出pdf报告")
        self.export_pdf.clicked.connect(lambda :( reporter.Reporter.to_pdf(QtWidgets.QFileDialog.getSaveFileName(self.Dialog,"输出路径",".")[0])

                                                  ,QMessageBox.information(self.Dialog, "message", "导出报告到完成")))



    def export_txt_(self):
        export_path = "./out.txt"

        export_path=QtWidgets.QFileDialog.getSaveFileName(self.Dialog,"输出路径",".")[0]
        if export_path == None or export_path == "":return
        colWidth=20
        f = open(export_path,'w',encoding="utf-8")
        ls = []
        ls.append("%s\t%s\t%s\r\n"%("违规描述".ljust(colWidth),"违规用例".ljust(colWidth),"违规句段".ljust(colWidth)))
        for e in self.data:
            ls.append("%s\t%s\t%s\r\n"%((e.rulename if e.rulename != None else "-").ljust(colWidth),e.usecasename.ljust(colWidth)
                                    ,(e.sentence.val if isinstance(e.sentence,rucmElement.Sentence) else str(e.sentence)).ljust(colWidth)))
        f.writelines(ls)
        f.close()
        QMessageBox.information(self.Dialog, "message", "导出报告到%s"%(export_path))

    def setVals(self):
        import os
        print(os.environ.get("Path"))
        # newItem = QTableWidgetItem('张三')
        # self.tableWidget.setItem(0, 0, newItem)
        self.data = copy.deepcopy(reporter.Reporter.errors)
        self.tableWidget.setRowCount(len(reporter.Reporter.errors))

        for i in range(3):
            self.tableWidget.setColumnWidth(i,250)
        for i,e in enumerate(reporter.Reporter.errors):
            self.tableWidget.setItem(i,0,QTableWidgetItem(e.rulename))
            self.tableWidget.setItem(i,1,QTableWidgetItem(e.usecasename))
            if isinstance(e.sentence,rucmElement.Sentence):
                self.tableWidget.setItem(i,2,QTableWidgetItem(e.sentence.val))
            else:
                self.tableWidget.setItem(i, 2, QTableWidgetItem(str(e.sentence)))

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




