#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ghostly峰'
__time__ = '2018/11/26 16:41'

from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt

#读取图像
img = cv2.imread('a.jpg')
#将图像转换为灰度图
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#阈值化处理
def  normalize1(data):
    m=data.shape[0]
    n=np.array(data).shape[1]
    x = np.array(data).shape[2]
    for k in range(x):
        for i in range(m):
            for j in range(n):
                if data[i,j,k]>=55:
                    data[i,j,k]=255
    return data


#自定义锐化操作
def custom_blur_demo(image):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32) #锐化
    dst = cv2.filter2D(image, -1, kernel=kernel)
    return dst

#直方图均衡化
def histogram_equalization(img):
    # img = custom_blur_demo(img)
    # 计算直方图
    hist, bins = np.histogram(img.flatten(), 256, [0, 256])
    # 计算分布函数F(a)
    cdf = hist.cumsum()
    cdf_normalized = cdf * float(hist.max()) / cdf.max()
    # 画直方图
    plt.plot(cdf_normalized, color='b')
    plt.hist(img.flatten(), 256, [0, 256], color='r')
    plt.show()

    # 把分布函数映射到[0,255]
    cdf = (cdf-cdf[0])*255/(cdf[-1]-1)
    cdf = cdf.astype(np.uint8)# Transform from float64 back to unit8

    # 均衡化以后的图像
    img3 = cdf[img]
    # 计算直方图
    hist1, bins1 = np.histogram(img3, 256)
    # 计算分布函数F(a)
    cdf1 = hist1.cumsum()
    cdf_normalized1 = cdf1 * float(hist.max()) / cdf1.max()
    # 画直方图
    plt.plot(cdf_normalized1, color='b')
    plt.hist(img3.flatten(), 256, [0, 256], color='r')
    plt.show()

    return img3


#中值滤波
img=cv2.medianBlur(img,3)

#锐化
img=cv2.blur(img,(3,3))

#获取形态学操作需要的核
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))

#腐蚀
erode = cv2.erode(img,kernel)

#膨胀
dilate = cv2.dilate(img,kernel,iterations = 1)

#将两幅图像相减获得边，第一个参数是膨胀后的图像，第二个参数是腐蚀后的图像
result = cv2.absdiff(dilate,erode)

#上面得到的结果是灰度图，将其二值化以便更清楚的观察结果
retval, result = cv2.threshold(result, 40, 255, cv2.THRESH_BINARY)

#反色，即对二值图每个像素取反
result = cv2.bitwise_not(result)

#开运算
img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

#闭运算
img0 = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

#将两张图像进行叠加
img = cv2.addWeighted(img0, 0.8, img, 0.35, 0)

#展示第一张图像
cv2.imshow("Image0", img0)
#展示第二张图像
cv2.imshow("Image", img)
#保持窗口状态
cv2.waitKey(0)
#销毁窗口
cv2.destroyAllWindows()