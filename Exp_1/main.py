from ui.bt_func import mywindow
from PyQt5 import QtWidgets
import sys


# Call show
app = QtWidgets.QApplication(sys.argv)
myshow = mywindow()
myshow.show()
sys.exit(app.exec_())
