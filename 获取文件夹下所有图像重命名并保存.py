#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ghostly峰'
__time__ = '2018/11/26 16:10'

import os
from PIL import Image
import numpy as np
#获取文件夹下所有文件名
# imageList = os.listdir('E:\Event\wuyuan_project\\xml2txt\labeling_result\data')
# imageList1 = os.listdir('E:\Event\wuyuan_project\\xml2txt\labeling_result\data_label')
#
# for index, i in enumerate(imageList):
#     img_path = i
#     print(img_path)
#     I = Image.open(f'E:\Event\wuyuan_project\\xml2txt\labeling_result\data\{img_path}')
#     I.save(f'E:\Event\wuyuan_project\\xml2txt\labeling_result\data1\{index}.jpg')

# data_tmp1 = Image.open('E:\Event\wuyuan_project\haar+adaboost\marman_ring_feature\\neg_data\\569.jpg')
#
# for index, item in enumerate(range(600, 900)):
#     data_tmp1 = data_tmp1.convert('RGB')
#     data_tmp1.save(f'E:\Event\wuyuan_project\haar+adaboost\marman_ring_feature\\neg_data\\{index+600}.jpg')
#     print(index)

#xml文件列表
imageList = os.listdir('E:\Event\wuyuan_project\\xml2txt\labeling_result\data_label')
# xml路径
path_xml = r'E:\Event\wuyuan_project\xml2txt\labeling_result\data_label'
# 图片路径
path_img = r'E:\Event\wuyuan_project\xml2txt\labeling_result\data'
# xml保存路径
save_xml = r'E:\Event\wuyuan_project\xml2txt\labeling_result\data_label1'
# 图片保存路径
save_img = r'E:\Event\wuyuan_project\xml2txt\labeling_result\data1'

for index, i in enumerate(imageList):
    print(index)
    x = i[:-4]
    # 打开文件
    src_xml = os.path.join(os.path.abspath(path_xml), x+'.xml')
    src_img = os.path.join(os.path.abspath(path_img), x+'.jpg')

    # 重命名
    dst_xml = os.path.join(os.path.abspath(save_xml), str(index) + '.xml')
    dst_img = os.path.join(os.path.abspath(save_img), str(index) + '.jpg')
    # 执行操作
    os.rename(src_xml, dst_xml)
    os.rename(src_img, dst_img)

