# -*- coding: utf-8 -*-
__author__ = 'ghostlyfeng'
__time__ = '2018/12/11 9:07'

#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import xml.dom.minidom
import os

load_dir = r'E:\Event\wuyuan_project\haar+adaboost\pos_data'

save_dir = r'E:\Event\wuyuan_project\haar+adaboost\pos_data_apogee_engine'
# save_dir_apogee_engine = r'E:\Event\wuyuan_project\haar+adaboost\pos_data_apogee_engine'
# save_dir_brackets_of_solar_panel = r'E:\Event\wuyuan_project\haar+adaboost\pos_data_brackets_of_solar_panel'
# save_dir_marman_ring = r'E:\Event\wuyuan_project\haar+adaboost\pos_data_marman_ring'
# save_dir_solar_panel = r'E:\Event\wuyuan_project\haar+adaboost\pos_data_solar_panel'


save_filename_apogee_engine = 'pos_data_apogee_engine.txt'
save_filename_brackets_of_solar_panel = 'pos_data_brackets_of_solar_panel.txt'
save_filename_marman_ring = 'pos_data_marman_ring.txt'
save_filename_solar_panel = 'pos_data_solar_panel.txt'


xmlList = os.listdir(load_dir)
f_apogee_engine = open(os.path.join(save_dir, save_filename_apogee_engine), 'w')
f_brackets_of_solar_panel = open(os.path.join(save_dir, save_filename_brackets_of_solar_panel), 'w')
f_marman_ring = open(os.path.join(save_dir, save_filename_marman_ring), 'w')
f_solar_panel = open(os.path.join(save_dir, save_filename_solar_panel), 'w')
all_objects_num = 0

def bbox(object):
    # 在这里获取bndbox， xmin等标签名的时候一定要看原始xml文件中是否有这些标签名
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
    return [leftTopX, leftTopY, length, width]

for i in xmlList:
    DOMTree = xml.dom.minidom.parse(f'{load_dir}\\{i}')
    annotation = DOMTree.documentElement

    filename = annotation.getElementsByTagName("filename")[0]

    if filename.childNodes[0].data[-3:] == 'jpg':
        imgname = filename.childNodes[0].data
    else:
        imgname = filename.childNodes[0].data + '.jpg'
    print(imgname)
    objects = annotation.getElementsByTagName("object")

    # apogee_engine = annotation.getElementsByTagName("apogee engine")
    # brackets_of_solar_panel = annotation.getElementsByTagName("brackets of solar panel")
    # marman_ring = annotation.getElementsByTagName("marman ring")
    # solar_panel = annotation.getElementsByTagName("solar panel")

    brackets_of_solar_panel_num = 0
    solar_panel_num = 0

    bboxLink = []

    #写solar panel的边界框文件
    for j in objects:
        name = j.getElementsByTagName("name")[0].childNodes[0].data
        if name == 'solar panel':
            solar_panel_num += 1
            b= bbox(j)
            bboxLink += b
    loc1 = [imgname] + [solar_panel_num] + bboxLink  # 文档保存格式：文件名 文件个数 坐标
    for i in range(len(loc1)):
        if solar_panel_num:
            f_solar_panel.write(str(loc1[i]) + ' ')
    if solar_panel_num:
        f_solar_panel.write('\t\n')
    bboxLink = []

    # 写brackets of solar panel的边界框文件
    for k in objects:
        name = k.getElementsByTagName("name")[0].childNodes[0].data
        if name == 'brackets of solar panel':
            brackets_of_solar_panel_num += 1
            b = bbox(k)
            bboxLink += b
    loc2 = [imgname] + [brackets_of_solar_panel_num] + bboxLink  # 文档保存格式：文件名 文件个数 坐标
    for i in range(len(loc2)):
        if brackets_of_solar_panel_num:
            f_brackets_of_solar_panel.write(str(loc2[i]) + ' ')
    if brackets_of_solar_panel_num:
        f_brackets_of_solar_panel.write('\t\n')

    # 写apogee engine的边界框文件
    loc3 = []
    for m in objects:
        name = m.getElementsByTagName("name")[0].childNodes[0].data
        if name == 'apogee engine':
            b = bbox(m)
            loc3 = [imgname] + [1] + b # 文档保存格式：文件名 文件个数 坐标
    for i in range(len(loc3)):
        f_apogee_engine.write(str(loc3[i]) + ' ')
    if loc3:
        f_apogee_engine.write('\t\n')

    # 写marman ring的边界框文件
    loc4 = []
    for n in objects:
        name = n.getElementsByTagName("name")[0].childNodes[0].data
        if name == 'marman ring':
            b = bbox(n)
            loc4 = [imgname] + [1] + b # 文档保存格式：文件名 文件个数 坐标
    for i in range(len(loc4)):
        f_marman_ring.write(str(loc4[i]) + ' ')
    if loc4:
        f_marman_ring.write('\t\n')

f_solar_panel.close()
f_brackets_of_solar_panel.close()
f_apogee_engine.close()
f_marman_ring. close()

