# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIntValidator,QDoubleValidator,QFont
from AddRule import Ui_Add_Dialog
from UserDetail import Ui_User_Detail_Dialog
from Report import Ui_Report_Dialog
import sys
from PyQt5.QtWidgets import QMessageBox
import argparse
from rucmLoader import RucmLoader
from reporter import Reporter
from RuleLoader import RuleLoader
import rule
import json
import nlputils#####
from copy import deepcopy
from AddRule2 import Ui_Add_Dialog
import re

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
        # 设置规则数量、rulePath、rucmPath等变量
        self.defaultRuleNum = 0
        self.userRuleNum = 0
        self.RUCMPath = ''
        self.rules = {}
        self.max_id = 0
        self.rulepath = ''
        # 设置默认规则表
        self.defaultTableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.defaultTableWidget.setGeometry(QtCore.QRect(50, 70, 361, 192))
        self.defaultTableWidget.setObjectName("defaultTableWidget")
        self.defaultTableWidget.setColumnCount(3)
        self.defaultTableWidget.setRowCount(self.defaultRuleNum)

        # 设置行头
        for i in range(self.defaultRuleNum):
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.defaultTableWidget.setVerticalHeaderItem(i, item)

        # 设置列头
        for i in range(3):
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.defaultTableWidget.setHorizontalHeaderItem(i, item)

        # 设置表项
        for i in range(self.defaultRuleNum):
            for j in range(3):
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                # 全部设置为不可编辑
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.defaultTableWidget.setItem(i, j, item)

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

        # 设置用户的表
        self.userTableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.userTableWidget.setGeometry(QtCore.QRect(490, 70, 361, 192))
        self.userTableWidget.setObjectName("userTableWidget")
        # 设置行列
        self.userTableWidget.setColumnCount(3)
        self.userTableWidget.setRowCount(self.userRuleNum)
        # 设置行头
        for i in range(self.userRuleNum):
            item = QtWidgets.QTableWidgetItem()
            self.userTableWidget.setVerticalHeaderItem(i, item)
        # 设置列头
        for i in range(3):
            item = QtWidgets.QTableWidgetItem()
            self.userTableWidget.setHorizontalHeaderItem(i, item)

        # 填表
        for i in range(self.userRuleNum):
            for j in range(3):
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                # 全部设置为不可编辑
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.userTableWidget.setItem(i, j, item)

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
        '''
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(310, 300, 131, 31))
        self.label_5.setFont(font)
        self.label_5.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label_5.setWordWrap(False)
        self.label_5.setIndent(0)
        self.label_5.setObjectName("label_5")
        '''
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
        item.setText(_translate("MainWindow", "描述"))
        __sortingEnabled = self.defaultTableWidget.isSortingEnabled()
        self.defaultTableWidget.setSortingEnabled(False)

        # default的序号设置，查看是附赠的，之后会由按钮替代掉
        for i in range(self.defaultRuleNum):
            item = self.defaultTableWidget.item(i, 0)
            item.setText(_translate("MainWindow", str(i+1)))
            item = self.defaultTableWidget.item(i, 2)
            item.setText(_translate("MainWindow", "查看"))

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
        # user的序号设置，查看是附赠的，之后会由按钮替代掉
        for i in range(self.userRuleNum):
            item = self.userTableWidget.item(i, 0)
            item.setText(_translate("MainWindow", str(i + 1)))

        self.userTableWidget.setSortingEnabled(__sortingEnabled)
        self.label_2.setText(_translate("MainWindow", "用户规则库"))
        self.RUCMLineEdit.setText(_translate("MainWindow", "请输入RUCM文件"))
        self.RUCMButton.setText(_translate("MainWindow", "选择文件"))
        self.label_3.setText(_translate("MainWindow", "RUCM文件"))
        self.addRuleButton.setText(_translate("MainWindow", "添加用户规则"))
        self.checkRuleButton.setText(_translate("MainWindow", "规则检查"))
        self.reportButton.setText(_translate("MainWindow", "查看报告"))
        self.label_4.setText(_translate("MainWindow", "控制命令"))
        '''self.label_5.setText(_translate("MainWindow", "设置ip"))'''
        self.saveRuleButton.setText(_translate("MainWindow", "保存规则库"))
        self.loadRuleButton.setText(_translate("MainWindow", "载入规则库"))

        # user的查看、启用、操作以及序号
        rowCount = self.defaultTableWidget.rowCount()
        for i in range(rowCount):
            self.defaultTableWidget.setCellWidget(i, 1, self.checkForRow(i, 0, True))

        rowCount = self.userTableWidget.rowCount()
        for i in range(rowCount):
            self.userTableWidget.setCellWidget(i, 2, self.buttonForRow(i, 1)) # 1 for user rule table
            self.userTableWidget.setCellWidget(i, 1, self.checkForRow(i, 1, True))
        # codes above are only used for debugging

        self.RUCMButton.clicked.connect(lambda: self.openfile(0))
        self.loadRuleButton.clicked.connect(lambda: self.openfile(1))
        self.saveRuleButton.clicked.connect(lambda: self.openfile(2))
        self.checkRuleButton.clicked.connect(self.check)
        self.reportButton.clicked.connect(self.report)
        self.addRuleButton.clicked.connect(self.addRule)
        self.houseNumEdit  = QtGui.QTextLine()

        # 加载默认规则
        self.loadRules('.\\rule-template.txt')
        '''
        # ip相关
        self.ipLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.ipLineEdit.setGeometry(QtCore.QRect(50, 300, 251, 41))
        self.ipLineEdit.setObjectName("RUCMLineEdit")
        self.ipLineEdit.textChanged.connect(self.get_url)
        self.ipLineEdit.setValidator(QIntValidator())
        self.ipLineEdit.setInputMask('00.000.0.000:0000;_')
        # 默认使用的是url
        self.ipLineEdit.setText(re.findall('\d+.\d+.\d+.\d+:\d+', nlputils.url)[0])
        '''
    '''
    # 获得ip
    def get_url(self, text):
        if len(text) >= len(r'00.000.0.000:9000'):
            pass
            # nlputils.url = 'http://' + text + '/'
            # print('更改ip为：' +  nlputils.url)
    '''
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
            deleteBtn.clicked.connect(lambda: self.deleteRuleTable(id))

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
    # initial_status = False 表示禁用， True 表示 启用
    def checkForRow(self, id, type, initial_status):
        widget=QtWidgets.QWidget()
        enable = QtWidgets.QCheckBox('启用')
        enable.setStyleSheet(''' text-align : center;
                                        height : 30px;
                                        border-style: outset;
                                        font : 13px; ''')
        if initial_status:
            enable.setCheckState(QtCore.Qt.Checked)
        enable.stateChanged.connect(lambda:self.checkEnable(id, type))
        hLayout = QtWidgets.QHBoxLayout()
        hLayout.addWidget(enable)
        hLayout.setContentsMargins(5,2,5,2)
        widget.setLayout(hLayout)
        return widget


    def openfile(self, type): # 0 for rucm file, 1 for load rule, 2 for save rule
        _translate = QtCore.QCoreApplication.translate
        
        if type == 0:  #RUCM
            openfile_name = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget,'选择文件','','RUCM File(*.rucm)')
            self.RUCMLineEdit.setText(_translate("MainWindow", openfile_name[0]))
            if len(openfile_name[0]) > 2:
                self.loadRUCM(openfile_name[0])
            # 如果没有中途取消，则会返回路径，否则，则会返回''
        elif type == 1:
            openfile_name = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget,'选择文件','','Rule File(*.txt)')
            if len(openfile_name[0]) > 2:
                self.loadRules(openfile_name[0])
        else:
            openfile_name = QtWidgets.QFileDialog.getSaveFileName(self.centralwidget,'保存文件','','Rule File(*.txt)')
            if len(openfile_name[0]) > 2:
                self.saveRules(openfile_name[0])

    '''TO DO LIST'''
    def updateRuleTable(self, id):
        # 和前面add rule的代码类似
        # id: row number
        # used to update the data of row id
        # only available for user rule table
        # 输入取那个规则
        input = self.rules['user-def'][id]
        Dialog = QtWidgets.QDialog()
        print(input)
        ui = Ui_Add_Dialog(input)
        ui.setupUi(Dialog)
        '''the second parameter should be a dict to wrap the rule detailes.
        It's some business related to RuleBase.'''
        Dialog.show()
        Dialog.exec_()
        output = input
        if output:
            output['id'] = self.rules['user-def'][id]['id']
            self.rules['user-def'][id] = output
        # 输出直接覆盖掉
        '''Consider how to save the changed rule details. 
        It's some business related to RuleBase'''


    def addRule(self, id):
        # id: row number
        # used to update the data of row id
        # only available for user rule table
        '''Consider how to save the added rule details. 
        It's some business related to RuleBase'''
        # 添加Ui_Add_Dialog返回值到dict
        input = {}
        Dialog = QtWidgets.QDialog()
        ui = Ui_Add_Dialog(input)
        ui.setupUi(Dialog)
        '''the second parameter should be None'''
        Dialog.show()
        Dialog.exec_()
        output = input
        if output:
            # id设置为已知的最大id + 1
            self.max_id = self.max_id + 1
            output['id'] = self.max_id
            print(output['id'])
            if 'user-def'not in self.rules:
                self.rules['user-def'] = []
            self.rules['user-def'].append(deepcopy(output))
            # 添加一个规则到界面
            self.__add_one_rule(1, True)
            _translate = QtCore.QCoreApplication.translate
            # 取出新加的规则设置
            rowCount = self.userTableWidget.rowCount()
            item = self.userTableWidget.item(rowCount - 1, 0)
            # 设置序号
            last_index = len(self.rules['user-def']) - 1
            item.setText(_translate("MainWindow", str(self.rules['user-def'][last_index]['id'])))

    def deleteRuleTable(self, id):
        # id: row number
        # used to delete the data of row id
        # only available for user rule table
        # 确认是否删除
        # 待添加

        # 移走行，然后userRuleNum - 1，重设index
        self.userTableWidget.removeRow(id)
        _translate = QtCore.QCoreApplication.translate
        self.userRuleNum = self.userRuleNum - 1
        self.userTableWidget.setRowCount(self.userRuleNum)

        # 在dict中将对应的规则的status设置为-1（因为如果直接删除会出错，#####可能会出错（由于-1）###########
        # 在绑定button函数的时候，id已经绑定了）。
        if self.rules:
            self.rules['user-def'][id]['status'] = -1
        '''Consider how to delete the deleted rule in RuleBase. '''

    def viewRuleTable(self, id, type):
        # id: row number  type: 0 for default rule table, 1 for user rule table
        # used to view the data of row id
        # 创建子窗口，传入dict中对应的那一条。
        content = ''
        if self.rules:
            if type == 0:
                if 'default' in self.rules:
                    content = self.rules['default'][id]
                    if content:
                        Dialog = QtWidgets.QDialog()
                        ui = Ui_Default_Detail_Dialog()
                        ui.setupUi(Dialog, content)
                        Dialog.show()
                        Dialog.exec_()
            else:
                if 'user-def' in self.rules:
                    content = self.rules['user-def'][id]
                    if content:
                        Dialog = QtWidgets.QDialog()
                        ui = Ui_User_Detail_Dialog()
                        ui.setupUi(Dialog, content)
                        Dialog.show()
                        Dialog.exec_()
            
            '''the second parameter should be a dict to wrap the rule detailes.
            It's some business related to RuleBase.'''


    def loadRUCM(self, file_path):
        # 直接将路径存储起来，等到了check的时候再一起load。
        self.RUCMPath = file_path

    def saveRules(self, file):
        # 存储路径
        self.rulepath = file
        rule_dict = deepcopy(self.rules)
        # 对删除的rule进行处理（statues设置为了-1）
        if 'user-def' in self.rules:
            l = len(rule_dict['user-def'])
            i = 0
            while i < l:
                if rule_dict['user-def'][i]['status'] == -1:
                    del rule_dict['user-def'][i]
                    l = l - 1
                i = i + 1
        # 对文件进行储存
        rule_json = json.dumps(rule_dict)
        f = open(file, 'wt+')
        f.write(rule_json)
        f.close()

    def loadRules(self, file):
        # 存储路径的同时，还要将rule存储到自身的dict中
        self.rulePath = file
        self.rules = json.load(open(self.rulePath, 'r'))
        # 这里应该需要检查一下格式#
        rule_loader = RuleLoader(self.rulePath)
        if not rule_loader.checkFileFormat():
            print('Wrong Format of Rule file')
            self.rulePath = ''
            self.rules = []
            return
        # 删除所有规则
        self.__delete_all_rule(self.userTableWidget, 1)
        self.__delete_all_rule(self.defaultTableWidget, 0)
        # 添加多条条用户规则
        # 首先重新设置表的行数
        defaultRuleNum = len(self.rules['default'])
        if 'user-def' in self.rules:
            userRuleNum = len(self.rules['user-def'])
        # 开始添加项
        _translate = QtCore.QCoreApplication.translate
        # 在加载完之后，要更新显示，主要是更新启用状态
        for i in range(defaultRuleNum):
            self.__add_one_rule(0, self.rules['default'][i]['status'])
            item = self.defaultTableWidget.item(i, 0)
            item.setText(_translate("MainWindow", str(self.rules['default'][i]['id'])))
            item = self.defaultTableWidget.item(i, 2)
            item.setText(_translate("MainWindow", str(self.rules['default'][i]['description'])))
        if 'user-def' in self.rules:
            for i in range(userRuleNum):
                self.__add_one_rule(1, self.rules['user-def'][i]['status'])
                item = self.userTableWidget.item(i, 0)
                item.setText(_translate("MainWindow", str(self.rules['user-def'][i]['id'])))
            self.max_id = self.rules['user-def'][i]['id']

    # 启用选项框
    def checkEnable(self, id, type):
        # Once the enabled state is changed, be sure to change the corresponding rule's enable attribute.
        # id: row number  type: 0 for default rule table, 1 for user rule table
        if self.rules:
            if type == 0:
                self.rules['default'][id]['status'] = not self.rules['default'][id]['status']
            else:
                self.rules['user-def'][id]['status'] = not self.rules['user-def'][id]['status']

    def check(self):
        # check the rucm file with rules.
        # Note there are some exceptions. For example, no rucm file or rules?

        # 清除RuleDB的所有规则
        rule.RuleDB.defaultRules = []
        rule.RuleDB.userRules = []
        # 清空error
        Reporter.errors = []
        # 先把rule加载到本地的一个./rule-template-tmp.txt文件中。
        # 然后把它传到saveRules
        self.rulepath = './rule-template-tmp.txt'
        self.saveRules(self.rulepath)

        if self.rulepath:
            print('Loading rule file: %s' % (self.rulepath))
            try:
                rule_load = RuleLoader(self.rulepath)
                rule_load.load()
                print(f'Load successfully! Result: \n{rule_load}')
            except (FileNotFoundError, json.JSONDecodeError) as err:
                print(err)
        else:
            print('No rule file is specified. Default rules are loaded only.')

        rucm_loader = None
        # load rucm
        if self.RUCMPath:
            print('Checking rucm file: %s' % (self.RUCMPath))
            #rucm_loader = RucmLoader(self.RUCMPath)
            print(f'Load successfully! Result: \n{rucm_loader}')
        else:
            print('No rucm file is given. Check rule file only.')

        print('---' * 65)
        if rucm_loader and rule_load:
            print('--------------check processing-------------')
            print(rule.RuleDB.userRules)
            print(rule.RuleDB.defaultRules)
            for i in rule.RuleDB.userRules:
                print('---', i.check)
                i.check()
            for i in rule.RuleDB.defaultRules:
                print('---', i.check)
                i.check()

    def report(self):

        Dialog = QtWidgets.QDialog()
        ui = Ui_Report_Dialog()
        ui.setupUi(Dialog)
        '''the second parameter should be a dict to wrap the rule detailes.
        It's some business related to RuleBase.'''
        Dialog.show()
        Dialog.exec_()

    # 在type的table里头添加一条规则，同时增加Num
    # init_status用来设置启用禁用，True表示启用
    def __add_one_rule(self, type, init_status=True):
        # 创建项
        if type == 0:
            i = self.defaultTableWidget.rowCount()
            self.defaultTableWidget.setRowCount(i + 1)
            for j in range(3):
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.defaultTableWidget.setItem(i, j, item)
        else:
            i = self.userTableWidget.rowCount()
            self.userTableWidget.setRowCount(i + 1)
            for j in range(3):
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.userTableWidget.setItem(i, j, item)
        # 链接函数
        if type == 0:
            self.defaultTableWidget.setCellWidget(i, 1, self.checkForRow(i, 0, init_status))
            self.defaultRuleNum = self.defaultRuleNum + 1
        elif type == 1:
            self.userTableWidget.setCellWidget(i, 2, self.buttonForRow(i, 1)) # 1 for user rule table
            self.userTableWidget.setCellWidget(i, 1, self.checkForRow(i, 1, init_status))
            self.userRuleNum = self.userRuleNum + 1

    def __delete_all_rule(self, table, type):
        if type == 0:
            for i in range(self.defaultRuleNum):
                self.defaultTableWidget.removeRow(0)
            self.defaultTableWidget.setRowCount(0)
            self.defaultRuleNum = 0
        elif type == 1:
            pass
            for i in range(self.userRuleNum):
                self.userTableWidget.removeRow(0)
            self.userTableWidget.setRowCount(0)
            self.userRuleNum = 0

class RuleBase:
    # A class for wrapping the details of each rule.
    rules = []
    def addRule(self, rule):
        # add a rule to the database
        pass

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