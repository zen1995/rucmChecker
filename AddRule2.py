# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddRule2.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication
import PyQt5
import sys
from PyQt5.QtCore import QCoreApplication
import copy
class Ui_MainWindow(object):

    def __init__(self,retVal):
        self.retVal = retVal
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(828, 462)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.box_applyScope = QtWidgets.QComboBox(self.centralwidget)
        self.box_applyScope.setGeometry(QtCore.QRect(80, 170, 69, 22))
        self.box_applyScope.setObjectName("box_applyScope")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(90, 140, 54, 12))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(210, 140, 54, 12))
        self.label_2.setObjectName("label_2")
        self.box_subject = QtWidgets.QComboBox(self.centralwidget)
        self.box_subject.setGeometry(QtCore.QRect(210, 170, 69, 22))
        self.box_subject.setObjectName("box_subject")
        self.box_op = QtWidgets.QComboBox(self.centralwidget)
        self.box_op.setGeometry(QtCore.QRect(320, 170, 101, 22))
        self.box_op.setObjectName("box_op")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(340, 140, 54, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(520, 140, 54, 12))
        self.label_4.setObjectName("label_4")
        self.line_val = QtWidgets.QLineEdit(self.centralwidget)
        self.line_val.setGeometry(QtCore.QRect(460, 170, 201, 20))
        self.line_val.setObjectName("line_val")
        self.box_description = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.box_description.setGeometry(QtCore.QRect(70, 240, 591, 71))
        self.box_description.setObjectName("box_description")
        self.buttonBox = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setGeometry(QtCore.QRect(470, 390, 156, 23))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.init_val()
    def init_val(self):
        applyScopes = {"所有句子":"allSentence","动作句子":"actionStep"}
        for k,v in applyScopes.items():
            self.box_applyScope.addItem(k,v)


        applyTarget = {"主语的数量":"subject_count","主语的值":"subject_Val","宾语的值":"object_Val","宾语的数量":"object_count",
                       "动词的数量":"verb_count","动词的时态":"verb_tense","句子中所有词语":"strs","情态动词的数量":"modal_verb_count",
                       "副词的数量":"adverb_count","代词的数量":"pronoun_count"}
        for k,v in applyTarget.items():
            self.box_subject.addItem(k,v)


        ops = {"在":"in","不在":"notIn","大于等于":"ge","大于":"gt","小于":"lt","小于等于":"le","等于":"eq","不等于":"neq"}
        for k,v in ops.items():
            self.box_op.addItem(k,v)

        if self.retVal != {}:
            if self.retVal["simpleRules"][0]["operation"] in ops.values():
                self.box_op.setCurrentIndex(list(ops.values()).index(self.retVal["simpleRules"][0]["operation"]))
            if self.retVal["simpleRules"][0]["subject"] in applyTarget.values():
                self.box_subject.setCurrentIndex(list(applyTarget.values()).index(self.retVal["simpleRules"][0]["subject"]))


            if self.retVal["applyScope"] in applyScopes.values():
                self.box_applyScope.setCurrentIndex(list(applyScopes.values()).index(self.retVal["applyScope"]))
            self.line_val.setText(str(self.retVal["simpleRules"][0]["val"])[1:-1])
            self.box_description.setPlainText(str(self.retVal["description"]))

        self.buttonBox.accepted.connect(self.finishEdit)
        self.buttonBox.rejected.connect(self.cancelEdit)
        self.retVal.clear()
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "作用范围"))
        self.label_2.setText(_translate("MainWindow", "作用对象"))
        self.label_3.setText(_translate("MainWindow", "作用操作"))
        self.label_4.setText(_translate("MainWindow", "值"))

    def finishEdit(self):
        print("finish Edit!")
        data = {
            "id":-1,"status":True,"applyScope":self.box_applyScope.currentData(),
            "simpleRules":[{"subject":self.box_subject.currentData(),
                           "operation":self.box_op.currentData(),
                           "val":eval("["+self.line_val.text()+"]")
                           }],"operation":"-","description":self.box_description.document().toPlainText()
        }
        for k,v in data.items():
            self.retVal[k]=v
        QCoreApplication.instance().quit()


    def cancelEdit(self):
        print("cancel!")
        QCoreApplication.instance().quit()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    r = {'id': -1, 'status': True, 'applyScope': "actionStep",
         'simpleRules': [{'subject': 'pronoun_count', 'operation': 'ge', 'val': ["111"]}], 'operation': '-', 'description': 'ff'}
    r = {}
    mainWindow = Ui_MainWindow(r)
    window = PyQt5.QtWidgets.QMainWindow()
    mainWindow.setupUi(window)

    window.show()
    print(app.exec_())
    print(r)
