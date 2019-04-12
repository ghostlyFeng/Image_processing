#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ghostly峰'
__time__ = '2018/11/26 16:59'

import os
from PIL import Image
import cv2
#获取文件夹下所有文件名
dir_path = 'E:\\Event\\五院项目\\haar+adaboost\\负样本'
imageList = os.listdir(dir_path)

for index, i in enumerate(imageList):
    img_path = i
    img = cv2.imread(f'{dir_path}{img_path}')
    img = img[:, int((img.shape[1]/2)-(img.shape[0]/2)):int((img.shape[1]/2)+(img.shape[0]/2)), :]
    cv2.imwrite(f'{dir_path}{img_path}', img)
    print(index)