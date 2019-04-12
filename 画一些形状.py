#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ghostly峰'
__time__ = '2018/11/29 19:53'

import cv2
import numpy as np

# 建立一张空白的图像
img = np.zeros((512, 512, 3), dtype=np.uint8)

# 画线
# 图像，起点坐标，终点坐标，颜色，线的宽度
cv2.line(img, (10, 10), (510, 510), (0, 255, 0), 5)

# 画圆
# img:图像，圆心坐标，圆半径，颜色，线宽度(-1：表示对封闭图像进行内部填满)
cv2.circle(img, (50, 50), 10, (0, 0, 255), -1)

# 画矩形
# img:图像,起点坐标,终点坐标,颜色,线宽度
cv2.rectangle(img, (70, 80), (90, 100), (255, 0, 0), -1)


# 画椭圆
# img:图像,中心坐标，长短轴长度(长轴长度,短轴长度),旋转角度,显示的部分(0:起始角度,180:终点角度),颜色，线宽度
cv2.ellipse(img, (150, 150), (10, 5), 0, 0, 180, (0, 127, 0), -1)

# 画多边形
# img:图像,顶点集，是否闭合，颜色，线宽度
Pts = np.array([[10, 5], [20, 30], [70, 20], [50, 10]], np.int32)
Pts = Pts.reshape((-1, 1, 2))
cv2.polylines(img, [Pts], True, (0, 255, 255), 33)

# 写入字符
# img：图像，输入字符串，坐标，字体，字号，颜色，颜色，线宽度，线条种类。
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img, 'HXH', (50, 300), font, 4, (255, 0, 255), 2, cv2.LINE_AA)

cv2.imshow('drawing.png', img)
cv2.waitKey(0)