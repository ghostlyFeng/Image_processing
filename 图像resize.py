#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ghostly峰'
__time__ = '2018/11/26 19:47'

from PIL import Image
import numpy as np
import cv2
import os
#获取文件夹下所有文件名
dir_path = 'E:\\Event\\五院项目\\haar+adaboost\\负样本'
imageList = os.listdir(dir_path)

for index, i in enumerate(imageList):
    data_tmp1 = Image.open(f'{dir_path}\\{i}')
    data_tmp2 = data_tmp1.resize((1440, 1440))
    data_tmp2.save(f'E:\\Event\\五院项目\\haar+adaboost\\负样本\\img_resize\\{index}.png')
    print(index)

