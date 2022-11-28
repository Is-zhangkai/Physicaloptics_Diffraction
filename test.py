# -*- coding: utf-8 -*-
# @Time    : 2022/11/7 16:58
# @Author  : zhangkai
# @File    : test.py
# @Software: PyCharm

import numpy as np
import matplotlib.pyplot as plt
import sys
import cv2
import Function as fun
from scipy import signal

if __name__ == '__main__':
    imgageIn = cv2.imread('Diffraction.jpg')
    # print(imgageIn)
    h = imgageIn.shape[0]
    w = imgageIn.shape[1]
    c = imgageIn.shape[2]
    if c == 3:
        imgageIn=cv2.cvtColor(imgageIn, cv2.COLOR_BGR2GRAY)
        imgageIn = np.double(imgageIn / 255)

    mylambda=532E-6     #波长
    k=2*np.pi/mylambda

    dp=5E-3

    img,k=fun.propagation_TF(imgageIn,mylambda,dp,100)
    img=fun.propagation_Len(img,k,dp,50,5)
    img,k=fun.propagation_TF(img,mylambda,dp,100)

    imgout=np.abs(img)

    print("ASdga")
    plt.imshow(imgout, cmap="gray")
    plt.show()
