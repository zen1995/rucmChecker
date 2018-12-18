# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from AddRule import Ui_Add_Dialog
from Detail import Ui_Detail_Dialog
from Report import Ui_Report_Dialog
import sys
class Ui_MainWindow(object):
    def setupUi(self, MainWindow, ruleBase, reporter):
        # RuleBase should be initialized.
        # reporter should be initialized.
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 482)
        self.ruleBase = ruleBase
        self.reporter = reporter
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.defaultTableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.defaultTableWidget.setGeometry(QtCore.QRect(50, 70, 361, 192))
        self.defaultTableWidget.setObjectName("defaultTableWidget")
        self.defaultTableWidget.setColumnCount(3)
        self.defaultTableWidget.setRowCount(2)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.defaultTableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.defaultTableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.defaultTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.defaultTableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.defaultTableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.defaultTableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.defaultTableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.defaultTableWidget.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.defaultTableWidget.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.defaultTableWidget.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.defaultTableWidget.setItem(1, 2, item)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 40, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label.setWordWrap(False)
        self.label.setIndent(0)
        self.label.setObjectName("label")
        self.userTableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.userTableWidget.setGeometry(QtCore.QRect(490, 70, 361, 192))
        self.userTableWidget.setObjectName("userTableWidget")
        self.userTableWidget.setColumnCount(3)
        self.userTableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.userTableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.userTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.userTableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.userTableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.userTableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.userTableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.userTableWidget.setItem(0, 2, item)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(490, 40, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label_2.setWordWrap(False)
        self.label_2.setIndent(0)
        self.label_2.setObjectName("label_2")
        self.RUCMLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.RUCMLineEdit.setGeometry(QtCore.QRect(50, 380, 251, 41))
        self.RUCMLineEdit.setObjectName("RUCMLineEdit")
        self.RUCMButton = QtWidgets.QPushButton(self.centralwidget)
        self.RUCMButton.setGeometry(QtCore.QRect(310, 380, 101, 41))
        self.RUCMButton.setObjectName("RUCMButton")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(50, 350, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label_3.setWordWrap(False)
        self.label_3.setIndent(0)
        self.label_3.setObjectName("label_3")
        self.addRuleButton = QtWidgets.QPushButton(self.centralwidget)
        self.addRuleButton.setGeometry(QtCore.QRect(750, 270, 101, 41))
        self.addRuleButton.setObjectName("addRuleButton")
        self.checkRuleButton = QtWidgets.QPushButton(self.centralwidget)
        self.checkRuleButton.setGeometry(QtCore.QRect(490, 380, 101, 41))
        self.checkRuleButton.setObjectName("checkRuleButton")
        self.reportButton = QtWidgets.QPushButton(self.centralwidget)
        self.reportButton.setGeometry(QtCore.QRect(620, 380, 101, 41))
        self.reportButton.setObjectName("reportButton")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(490, 350, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(18)
        self.label_4.setFont(font)
        self.label_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label_4.setWordWrap(False)
        self.label_4.setIndent(0)
        self.label_4.setObjectName("label_4")
        self.saveRuleButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveRuleButton.setGeometry(QtCore.QRect(490, 270, 101, 41))
        self.saveRuleButton.setObjectName("saveRuleButton")
        self.loadRuleButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadRuleButton.setGeometry(QtCore.QRect(620, 270, 101, 41))
        self.loadRuleButton.setObjectName("loadRuleButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        '''
        item = self.defaultTableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "default 1"))
        item = self.defaultTableWidget.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "default 2"))
        '''
        item = self.defaultTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "序号"))
        item = self.defaultTableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "启用"))
        item = self.defaultTableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "操作"))
        __sortingEnabled = self.defaultTableWidget.isSortingEnabled()
        self.defaultTableWidget.setSortingEnabled(False)

        # codes below are only used for debugging        
        item = self.defaultTableWidget.item(0, 0)
        item.setText(_translate("MainWindow", "1"))
        item = self.defaultTableWidget.item(0, 2)
        item.setText(_translate("MainWindow", "查看"))
        item = self.defaultTableWidget.item(1, 0)
        item.setText(_translate("MainWindow", "1"))
        item = self.defaultTableWidget.item(1, 2)
        item.setText(_translate("MainWindow", "查看"))
        # codes above are only used for debugging

        self.defaultTableWidget.setSortingEnabled(__sortingEnabled)
        self.label.setText(_translate("MainWindow", "默认规则库"))
        '''
        item = self.userTableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "用户规则1"))
        '''
        item = self.userTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "序号"))
        item = self.userTableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "启用"))
        item = self.userTableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "操作"))
        __sortingEnabled = self.userTableWidget.isSortingEnabled()
        self.userTableWidget.setSortingEnabled(False)
        item = self.userTableWidget.item(0, 0)
        item.setText(_translate("MainWindow", "1"))
        self.userTableWidget.setSortingEnabled(__sortingEnabled)
        self.label_2.setText(_translate("MainWindow", "用户规则库"))
        self.RUCMLineEdit.setText(_translate("MainWindow", "请输入RUCM文件"))
        self.RUCMButton.setText(_translate("MainWindow", "选择文件"))
        self.label_3.setText(_translate("MainWindow", "RUCM文件"))
        self.addRuleButton.setText(_translate("MainWindow", "添加用户规则"))
        self.checkRuleButton.setText(_translate("MainWindow", "规则检查"))
        self.reportButton.setText(_translate("MainWindow", "查看报告"))
        self.label_4.setText(_translate("MainWindow", "控制命令"))
        self.saveRuleButton.setText(_translate("MainWindow", "保存规则库"))
        self.loadRuleButton.setText(_translate("MainWindow", "载入规则库"))

        # codes below are only used for debugging
        rowCount = self.defaultTableWidget.rowCount()
        for i in range(rowCount):
            self.defaultTableWidget.setCellWidget(i, 2, self.buttonForRow(i, 0)) # 0 for default rule table
            self.defaultTableWidget.setCellWidget(i, 1, self.checkForRow(i, 0)) 
        rowCount = self.userTableWidget.rowCount()
        for i in range(rowCount):
            self.userTableWidget.setCellWidget(i, 2, self.buttonForRow(i, 1)) # 1 for user rule table
            self.userTableWidget.setCellWidget(i, 1, self.checkForRow(i, 1))        
        # codes above are only used for debugging

        self.RUCMButton.clicked.connect(lambda: self.openfile(0))
        self.loadRuleButton.clicked.connect(lambda: self.openfile(1))
        self.saveRuleButton.clicked.connect(lambda: self.openfile(2))
        self.checkRuleButton.clicked.connect(self.check)
        self.reportButton.clicked.connect(self.report)
        self.addRuleButton.clicked.connect(self.addRule)

    # 列表内添加按钮
    def buttonForRow(self,id, type):
        widget=QtWidgets.QWidget()
        
        # 查看
        viewBtn = QtWidgets.QPushButton('查看')
        viewBtn.setStyleSheet(''' text-align : center;
                                  background-color : DarkSeaGreen;
                                  height : 30px;
                                  border-style: outset;
                                  font : 13px; ''')

        viewBtn.clicked.connect(lambda: self.viewRuleTable(id, type))
        if type:
            # 删除
            deleteBtn = QtWidgets.QPushButton('删除')
            deleteBtn.setStyleSheet(''' text-align : center;
                                        background-color : LightCoral;
                                        height : 30px;
                                        border-style: outset;
                                        font : 13px; ''')
            deleteBtn.clicked.connect(lambda:self.deleteRuleTable(id))

            # 修改
            updateBtn = QtWidgets.QPushButton('修改')
            updateBtn.setStyleSheet(''' text-align : center;
                                              background-color : NavajoWhite;
                                              height : 30px;
                                              border-style: outset;
                                              font : 13px  ''')

            updateBtn.clicked.connect(lambda:self.updateRuleTable(id))

        hLayout = QtWidgets.QHBoxLayout()
        hLayout.addWidget(viewBtn)
        if type:
            hLayout.addWidget(updateBtn)
            hLayout.addWidget(deleteBtn)
        hLayout.setContentsMargins(5,2,5,2)
        widget.setLayout(hLayout)
        return widget

    # 列表内添加选择按钮
    def checkForRow(self, id, type):
        widget=QtWidgets.QWidget()
        enable = QtWidgets.QCheckBox('启用')
        enable.setStyleSheet(''' text-align : center;
                                        height : 30px;
                                        border-style: outset;
                                        font : 13px; ''')
        enable.setCheckState(QtCore.Qt.Unchecked)
        enable.stateChanged.connect(lambda:self.checkEnable(id, type))
        hLayout = QtWidgets.QHBoxLayout()
        hLayout.addWidget(enable)
        hLayout.setContentsMargins(5,2,5,2)
        widget.setLayout(hLayout)
        return widget


    def openfile(self, type): # 0 for rucm file, 1 for load rule, 2 for save rule
        _translate = QtCore.QCoreApplication.translate
        
        if type == 0: 
            openfile_name = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget,'选择文件','','RUCM File(*.rucm)')
            self.RUCMLineEdit.setText(_translate("MainWindow", openfile_name[0]))
        elif type == 1:
            openfile_name = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget,'选择文件','','Rule File(*.txt)')
            self.loadRules(openfile_name)
        else:
            openfile_name = QtWidgets.QFileDialog.getSaveFileName(self.centralwidget,'保存文件','','Rule File(*.txt)')
            self.saveRules(openfile_name)

    '''TO DO LIST'''
    def updateRuleTable(self, id):
        # id: row number
        # used to update the data of row id
        # only available for user rule table
        Dialog = QtWidgets.QDialog()
        ui = Ui_Add_Dialog()
        ui.setupUi(Dialog, None) 
        '''the second parameter should be a dict to wrap the rule detailes.
        It's some business related to RuleBase.'''
        Dialog.show()
        Dialog.exec_()
        '''Consider how to save the changed rule details. 
        It's some business related to RuleBase'''

    def addRule(self, id):
        # id: row number
        # used to update the data of row id
        # only available for user rule table
        Dialog = QtWidgets.QDialog()
        ui = Ui_Add_Dialog()
        ui.setupUi(Dialog, None) 
        '''the second parameter should be None'''
        Dialog.show()
        Dialog.exec_()
        '''Consider how to save the added rule details. 
        It's some business related to RuleBase'''

    def deleteRuleTable(self, id):
        # id: row number
        # used to delete the data of row id
        # only available for user rule table
        self.userTableWidget.removeRow(id)
        '''Consider how to delete the deleted rule in RuleBase. '''

    def viewRuleTable(self, id, type):
        # id: row number  type: 0 for default rule table, 1 for user rule table
        # used to view the data of row id
        Dialog = QtWidgets.QDialog()
        ui = Ui_Detail_Dialog()
        ui.setupUi(Dialog, None) 
        '''the second parameter should be a dict to wrap the rule detailes.
        It's some business related to RuleBase.'''
        Dialog.show()
        Dialog.exec_()

    def saveRules(self, file):
        # Save all the rules in a RuleBase to a rule-template file.
        pass

    def loadRules(self, file):
        # Load all the rules to a RuleBase from a rule-template file.
        pass
    
    def checkEnable(self, id, type):
        # Once the enabled state is changed, be sure to change the corresponding rule's enable attribute.
        # id: row number  type: 0 for default rule table, 1 for user rule table
        pass
    
    def check(self):
        # check the rucm file with rules.
        # Note there are some exceptions. For example, no rucm file or rules?
        pass

    def report(self):
        Dialog = QtWidgets.QDialog()
        ui = Ui_Report_Dialog()
        ui.setupUi(Dialog, self.reporter) 
        '''the second parameter should be a dict to wrap the rule detailes.
        It's some business related to RuleBase.'''
        Dialog.show()
        Dialog.exec_()

class RuleBase:
    # A class for wrapping the details of each rule.
    rules = []
    def addRule(self, rule):
        # add a rule to the database
        pass

    '''找泽年设计方法去'''

class ComplexRule:
    rules = []
    _type = False  # True for user rule, False for default rule.
    id = -1 # Rule id
    description = '' # Rule description
    linkSymbol = [] # The logic operation among simple rules.
    enable = False
    '''找泽年设计方法去'''

class SimpleRule:
    subject = '' # Rule subject. It should have an enum type to list all the subjects.
    value = [] # Rule value.
    op = '' # Rule operation. It should have an enum type to list all the operations.
    '''找泽年设计方法去'''

class Report:
    '''不造啥格式 你们自己设计'''
    pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv) 
    MainWindow = QtWidgets.QMainWindow()
    ruleBase = RuleBase()
    report = Report()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, ruleBase, report)
    MainWindow.show()  
    sys.exit(app.exec_()) 