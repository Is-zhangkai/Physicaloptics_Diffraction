
# -*- coding: utf-8 -*-
# @Time    : 2022/11/26
# @Author  : zhangkai
# @File    : main.py
# @Software: PyCharm
"""
主函数，打开主界面
"""

import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from Package import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mywindow = MainWindow()
    mywindow.setWindowTitle("Physicaloptics_Diffraction")
    mywindow.setWindowIcon(QIcon("./icon.ico"))
    mywindow.show()
    sys.exit(app.exec_())