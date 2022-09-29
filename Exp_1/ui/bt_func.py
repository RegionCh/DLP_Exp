from PyQt5 import QtWidgets
from ui.Ref_bib_Download import Ui_Mainwindow


# 这个类继承界面UI类
class mywindow(QtWidgets.QWidget, Ui_Mainwindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)

    # 定义槽函数
    def Path(self):
        FilePath = self.lineEdit.text()
        print(FilePath)

