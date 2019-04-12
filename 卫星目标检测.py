from __future__ import print_function
__author__ = 'ghostlyfeng'
__time__ = '2018/12/10 15:22'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import cv2 as cv
import argparse
def detectAndDisplay(img):
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_gray = cv.equalizeHist(img_gray)
    #-- Detect faces
    objects = object_cascade.detectMultiScale(img_gray)
    for (x,y,w,h) in objects:
        img = cv.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        imgROI = img_gray[y:y+h,x:x+w]
    cv.imshow('Img', img)
parser = argparse.ArgumentParser(description='Code for Cascade Classifier tutorial.')

#这里的default路径要设为OpenCV源文件夹下的文件路径
parser.add_argument('--object_cascade', help='Path to cascade.', default='E:\Event\wuyuan_project\haar+adaboost\marman_ring_feature\\xml_LBP\\cascade.xml')

args = parser.parse_args()
object_cascade_name = args.object_cascade
print(object_cascade_name)
object_cascade = cv.CascadeClassifier()
#-- 1. Load the cascades
if not object_cascade.load(object_cascade_name):
    print('--(!)Error loading face cascade')
    exit(0)

#这里路径中不能出现中文
img = cv.imread('E:\Event\wuyuan_project\haar+adaboost\\test_data\\b.jpg')
start = time.time()
detectAndDisplay(img)
end = time.time()
print('耗时：', end - start)
cv.waitKey(0)
