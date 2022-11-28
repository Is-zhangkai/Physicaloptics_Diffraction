# -*- coding: utf-8 -*-
# @Time    : 2022/9/19 20:53
# @Author  : zhangkai
# @File    : Package.py
# @Software: PyCharm

"""



"""
import os

from PIL import Image

from diffraction import Ui_MainWindow
import matplotlib
import numpy as np
import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QFileDialog, QGraphicsPixmapItem

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import Function as fun

matplotlib.use("Qt5Agg")



class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.imageIn = None
        self.image_out=None
        self.setupUi(self)

        self.dp = 5E-3
        self.btn_loadpic.clicked.connect(self.load_file)
        self.btn_showOutput.clicked.connect(self.ShowOutImg)
        self.checkBox_focusing.clicked.connect(self.CheckBox)

        self.btn_showOutput.setEnabled(False)


        self.horizontalSlider_objectd.setValue(int(self.lineEdit_objectd.text()))
        self.horizontalSlider_focald.setValue(int(self.lineEdit_focald.text()))
        self.horizontalSlider_Imaged.setValue(int(self.lineEdit_Imaged.text()))

        self.lineEdit_objectd.textChanged.connect(self.LE_Objectd)
        self.lineEdit_focald.textChanged.connect(self.LE_Focald)
        self.lineEdit_Imaged.textChanged.connect(self.LE_Imaged)
        self.horizontalSlider_objectd.valueChanged.connect(self.HS_Objectd)
        self.horizontalSlider_focald.valueChanged.connect(self.HS_Focald)
        self.horizontalSlider_Imaged.valueChanged.connect(self.HS_Imaged)


    def load_file(self):

        try:

            filename = QFileDialog.getOpenFileNames(self, '选择图像', os.getcwd(), "All Files(*);;Text Files(*.txt)")
            # 输出文件，查看文件路径
            print(filename)
            if  filename  is not None:


                self.btn_showOutput.setEnabled(True)
                self.imageIn = cv2.imread(filename[0][0])
                try:
                    self.imageIn = cv2.cvtColor(self.imageIn, cv2.COLOR_BGR2GRAY)
                except:
                    print("not RGB")
                self.show_image(self.imageIn, self.graphicsView_imageIn)
                self.imageoo = self.imageIn

                self.imageIn = self.imageIn.astype(float) / 255
        except:
            print("error：load_file")
    def ShowOutImg(self):
        try:
            self.propagation_BeforeLens()

            self.propagation_Lens()
            self.propagation_ImageOut()


        except:
            print("error:ShowOutImg")

    def propagation_BeforeLens(self):
        try:
            self.mylambda = int(self.lineEdit_lambda.text()) * 1E-6
            self.d_object = float(self.lineEdit_objectd.text())
            self.image_beforeLens, self.k = fun.propagation_TF(self.imageIn, self.mylambda, self.dp, self.d_object)

            print("finish:——————propagation_BeforeLens")
        except:
            print("error:propagation_BeforeLens")

    def propagation_Lens(self):
        try:

            self.focal = float(self.lineEdit_focald.text())
            self.radius = float(self.lineEdit_radius.text())
            self.image_afterLens = fun.propagation_Len(self.image_beforeLens, self.k, self.dp, self.focal, self.radius)
            print("finish:——————propagation_Lens")
        except:
            print("error:propagation_Lens")

    def propagation_ImageOut(self):
        try:

            if self.checkBox_focusing.isChecked():
                self.d_image = 1/( 1 / self.focal-1 / self.d_object )
                self.lineEdit_Imaged.setText(str(round(self.d_image)))

            else:
                self.d_image = float(self.lineEdit_Imaged.text())
            self.d_image = float(self.lineEdit_Imaged.text())

            self.image_out, self.k = fun.propagation_TF(self.image_afterLens, self.mylambda, self.dp, self.d_image)

            self.image_out = np.abs(self.image_out)
            self.image_out = (self.image_out - np.min(self.image_out)) / (np.max(self.image_out) - np.min(self.image_out))
            self.image_out = (self.image_out * 255).astype(np.uint8)
            # print(self.image_out.dtype)
            # print("dfghbsd")

            print("finish:——————propagation_ImageOut")

            cv2.imwrite("1.jpg", self.image_out)

            img = cv2.imread("1.jpg")
            try:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            except:
                print("sdfs")

            self.show_image( img, self.graphicsView_imageOut)
        except:
            print("error:propagation_ImageOut")

    def show_image(self, img, view):
        """
        :param img: image
        :param view: graphicsView
        :return: None
        """
        height, width = img.shape
        imgQ = QImage(img, width, height, QImage.Format_Indexed8)
        imgQPixmap = QPixmap.fromImage(imgQ).scaledToWidth(view.width() - 4)
        scene =QGraphicsScene()
        scene.clear()
        scene.addPixmap(imgQPixmap)
        view.setScene(scene)
        view.show()

    def CheckBox(self):

        if self.checkBox_focusing.isChecked():
           self.lineEdit_Imaged.setEnabled(False)
           self.horizontalSlider_Imaged.setEnabled(False)

        else:
            self.lineEdit_Imaged.setEnabled(True)
            self.horizontalSlider_Imaged.setEnabled(True)


    def LE_Objectd(self):
        try:
            d_object = int(self.lineEdit_objectd.text())
            if d_object > 0 and d_object <= 1000:
                self.horizontalSlider_objectd.setValue(d_object)
            else:
                print("数据输入错误")
        except:
            print("物距同步错误")

    def LE_Focald(self):
        try:
            d_focal = int(self.lineEdit_focald.text())
            if d_focal > 0 and d_focal <= 1000:
                self.horizontalSlider_focald.setValue(d_focal)
            else:
                print("数据输入错误")
        except:
            print("焦距同步错误")

    def LE_Imaged(self):
        try:
            d_imaged = int(self.lineEdit_Imaged.text())
            if d_imaged > 0 and d_imaged <= 1000:
                self.horizontalSlider_Imaged.setValue(d_imaged)
            else:
                print("数据输入错误")

        except:
            print("像距同步错误")

    def HS_Objectd(self):
        try:
            self.lineEdit_objectd.setText(str(self.horizontalSlider_objectd.value()))
            self.propagation_BeforeLens()
            self.propagation_Lens()
            self.propagation_ImageOut()
        except:
            print("物距同步错误")

    def HS_Focald(self):
        try:
            self.lineEdit_focald.setText(str(self.horizontalSlider_focald.value()))
            self.propagation_Lens()
            self.propagation_ImageOut()
        except:
            print("焦距同步错误")

    def HS_Imaged(self):
        try:
            self.lineEdit_Imaged.setText(str(self.horizontalSlider_Imaged.value()))
            self.propagation_ImageOut()

        except:
            print("像距同步错误")
