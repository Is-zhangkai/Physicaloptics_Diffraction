# -*- coding: utf-8 -*-
# @Time    : 2022/11/7 16:58
# @Author  : zhangkai
# @File    : test.py
# @Software: PyCharm

import numpy as np
import matplotlib.pyplot as plt
import sys
import cv2
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

    # cv2.imshow('ss',imgageIn)
    # cv2.waitKey()
    # cv2.destroyWindow()



    # print(imgageIn)
    # plt.imshow(imgageIn, cmap="gray")
    # plt.show()


    mylambda=532E-6     #波长
    k=2*np.pi/mylambda      #

    dp=5E-3
    sizexSLM = w*dp  # 空间光调制器尺寸
    sizeySLM = h*dp
    z = 260
    xx=np.arange(-sizexSLM/2,sizexSLM/2,dp)
    yy = np.arange(-sizeySLM / 2, sizeySLM / 2, dp)

    XX ,YY=np.meshgrid(xx,yy)
    h=np.exp(1j*k*(XX**2+YY**2)/(2*z))      #卷积核

    # img=signal.convolve2d(imgageIn,h,boundary='symm',mode='same')
    H=np.fft.fftshift(np.fft.fft2(h))
    F=np.fft.fft2(np.fft.fftshift(imgageIn))
    img=F*H
    img1=np.fft.fftshift(np.fft.ifft2(img))
    out=np.exp(1j*k*z*img1/(1j*mylambda*z))      #
    ot=np.abs(out)

    # outc=np.conj(out)
    # F=np.fft.fft2(np.fft.fftshift(outc))
    # res=F*H
    # opt=np.fft.fft2(np.fft.fftshift(res))
    plt.imshow(ot, cmap="gray")
    plt.show()




