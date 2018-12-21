from MainWindow import *
import sys

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ruleBase = RuleBase()
report = Report()
ui = Ui_MainWindow()
ui.setupUi(MainWindow, ruleBase, report)
MainWindow.show()
sys.exit(app.exec_())