# -*- coding: utf-8 -*-
# @Time    : 2022/11/27 13:04
# @Author  : zhangkai
# @File    : Function.py
# @Software: PyCharm

import numpy as np


def propagation_TF(imgageIn, wave_lambda, dp, distance):
    k = 2 * np.pi / wave_lambda
    slm_x = imgageIn.shape[1] * dp  # 空间光调制器尺寸
    slm_y = imgageIn.shape[0] * dp
    xx = np.arange(-slm_x / 2, slm_x / 2, dp)
    yy = np.arange(-slm_y / 2, slm_y / 2, dp)
    XX, YY = np.meshgrid(xx, yy)

    h = np.exp(1j * k * (XX ** 2 + YY ** 2) / (2 * distance))  # 卷积核

    H = np.fft.fft2(np.fft.fftshift(h))
    F = np.fft.fft2(np.fft.fftshift(imgageIn))

    image = np.fft.ifftshift(np.fft.ifft2(F * H))

    # image_out =image* np.exp(1j * k * distance)  / (1j * wave_lambda * distance)

    return image, k


def propagation_Len(imgage_in, k, dp, focal, size_len):
    sizex_SLM = imgage_in.shape[1] * dp
    sizey_SLM = imgage_in.shape[0] * dp
    xx = np.arange(-sizex_SLM / 2, sizex_SLM / 2, dp)
    yy = np.arange(-sizey_SLM / 2, sizey_SLM / 2, dp)
    XX, YY = np.meshgrid(xx, yy)

    lenses = np.exp(-1j * k * (XX ** 2 + YY ** 2) / (2 * focal)) * ((XX ** 2 + YY ** 2) < (size_len ** 2))
    image_out = imgage_in * lenses

    return image_out
