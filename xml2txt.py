#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import xml.dom.minidom
import os

load_dir = r'E:\Event\wuyuan_project\haar+adaboost\pos_data'
save_dir = r'E:\Event\wuyuan_project\haar+adaboost\pos_data_apogee_engine'
save_filename = 'pos_data_apogee_engine.txt'
if not os.path.exists(save_dir):
    os.mkdir(save_dir)

xmlList = os.listdir(load_dir)
f = open(os.path.join(save_dir, save_filename), 'w')
all_objects_num = 0
for i in xmlList:
    DOMTree = xml.dom.minidom.parse(f'{load_dir}\\{i}')
    annotation = DOMTree.documentElement

    filename = annotation.getElementsByTagName("filename")[0]

    imgname = filename.childNodes[0].data + '.jpg'
    print(imgname)
    objects = annotation.getElementsByTagName("object")
    lenObjects = [len(objects)]
    all_objects_num += len(objects)

    loc = [imgname] + lenObjects # 文档保存格式：文件名 文件个数 坐标


    for object in objects:

        #在这里获取bndbox， xmin等标签名的时候一定要看原始xml文件中是否有这些标签名
        bbox = object.getElementsByTagName("bndbox")[0]
        print('bbox', bbox)

        xmin = bbox.getElementsByTagName("xmin")[0]
        xmin = xmin.childNodes[0].data
        print('xmin', xmin)

        ymin = bbox.getElementsByTagName("ymin")[0]
        ymin = ymin.childNodes[0].data
        print('ymin', ymin)

        xmax = bbox.getElementsByTagName("xmax")[0]
        xmax = xmax.childNodes[0].data
        print('xmax', xmax)

        ymax = bbox.getElementsByTagName("ymax")[0]
        ymax = ymax.childNodes[0].data
        print('ymax', ymax)

        leftTopX = int(xmin)
        leftTopY = int(ymax)
        length = int(ymax) - int(ymin)
        width = int(xmax) - int(xmin)

        loc = loc + [leftTopX, leftTopY, length, width]

    # f.write(save_dir + '\\pos_data\\')
    for i in range(len(loc)):
        f.write(str(loc[i]) + ' ')
    f.write('\t\n')
f.close()
print(all_objects_num)