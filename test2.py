# -*- coding: utf-8 -*-
# @Time    : 2022/11/26 13:28
# @Author  : zhangkai
# @File    : test2.py
# @Software: PyCharm
import time

import numpy as np
import matplotlib.pyplot as plt
import sys
import cv2
from scipy import signal
import scipy.fft as fft
if __name__ == '__main__':
    tic = time.perf_counter()
    imgageIn = cv2.imread('Diffraction.jpg')
    # print(imgageIn)
    h = imgageIn.shape[0]
    w = imgageIn.shape[1]
    c = imgageIn.shape[2]
    if c == 3:
        imgageIn=cv2.cvtColor(imgageIn, cv2.COLOR_BGR2GRAY)
        imgageIn = np.double(imgageIn / 255)

        mylambda = 532E-6  # 波长
        k = 2 * np.pi / mylambda  #

        dp = 5E-3

        z = 100
        z2 = 100

        imgsrc = imgageIn.astype(float) / 255

        rowSize = w * dp # 空间光调制器尺寸
        colSize = h * dp

        rr = np.arange(-rowSize / 2, rowSize / 2, dp)
        cc = np.arange(-colSize / 2, colSize / 2, dp)
        RR, CC = np.meshgrid(rr, cc)

        srcFFT = fft.fft2(fft.fftshift(imgsrc))
        box1 = np.exp(1j * k * (RR ** 2 + CC ** 2) / (2 * z))
        box1FFT = fft.fft2(fft.fftshift(box1))
        dstMid = fft.ifftshift(fft.ifft2(srcFFT * box1FFT))
        # dstMid = dstMid * np.exp(1j * k * distanceEx) / (1j * waveLambda * distanceEx)
        # dstMid = np.exp((1j * k * z) * dstMid / (1j * mylambda * z))
        lenses = np.exp(-1j * k * (RR ** 2 + CC ** 2) / (2 * 50)) * ((RR ** 2 + CC ** 2) < 5)
        dstMid = dstMid * lenses

        box2 = np.exp(1j * k * (RR ** 2 + CC ** 2) / (2 * z2))
        box2FFT = fft.fft2(fft.fftshift(box2))
        dstMidFFT = fft.fft2(fft.fftshift(dstMid))
        dst = fft.ifftshift(fft.ifft2(dstMidFFT * box2FFT))
        # dst = dst * np.exp(1j * k * distanceAf) / (1j * waveLambda * distanceAf)
        # dst = np.exp((1j * k * z2) * dst / (1j * mylambda * z2))
        dst = np.abs(dst)
        dst = (dst - np.min(dst)) / (np.max(dst) - np.min(dst))
        dst = (dst * 255).astype(np.uint8)
        plt.imshow(dst, cmap="gray")

        toc = time.perf_counter()
        print(f"该程序耗时: {toc - tic:0.4f} seconds")
        plt.show()

