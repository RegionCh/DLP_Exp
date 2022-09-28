from ui.Ref_bib_Download import Ui_Mainwindow
from PyQt5 import QtWidgets
import sys


# 这个类继承界面UI类
class mywindow(QtWidgets.QWidget, Ui_Mainwindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)

#调用show
if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    myshow=mywindow()
    myshow.show()
    sys.exit(app.exec_())