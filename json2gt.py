import json
import numpy as np
import cv2
from PIL import Image
import os
import glob
import torch
from matplotlib import pyplot as plt

# 标注中的 x 轴是宽度，y轴是高度
# 所以 x1, y1, x2, y2 对应的是 left, top, right, bottom
# np.array之后的，以及cv2 read到 np的矩阵，排列方式是 高度，宽度，第一索引是top/bottom, 第二索引是left/right


def json2gt_word( jpath):
    '''
    将一个json文件中的整行坐标和单字坐标保存在buff中
    :param jpath:
    :return:
    '''
    jlist = json.load( open(jpath, "r") ) # jlist is : (remark in lengthN), char1, char2, charN
    buff = []
    remark = ''
    for index, item in enumerate(jlist):
        if item["remark"] != "ocr":
            remark += item["remark"].strip()
            buff.append((np.array([item["x1"], item["y1"], item["x2"], item["y2"]]).astype(np.int32), item["remark"].strip()))
        else:
            buff.append((np.array([item["x1"], item["y1"], item["x2"], item["y2"]]).astype(np.int32), remark[index-1]))
    # assert len(remark) == len(jlist)-1 , f"len remark: {len(remark)} while jlist is {len(jlist)-1}"

    return buff

def json2gt_line( jpath):
    '''
    将一个json文件中的整行坐标保存在buff中
    :param jpath:
    :return:
    '''
    jlist = json.load( open(jpath, "r") ) # jlist is : (remark in lengthN), char1, char2, charN
    buff = []
    remark = ''
    for index, item in enumerate(jlist):
            remark += item["remark"].strip()
            buff.append((np.array([item["x1"], item["y1"], item["x2"], item["y2"]]).astype(np.int32), item["remark"].strip()))
    return buff

def draw_path2img(img, gts, ignore_first=False):
    '''
    将边界框标注在图像上面并显示
    :param img_path:
    :param json_path:
    :param ignore_first:
    :return:
    '''
    if ignore_first:
        gts = gts[1:]
    for gt in gts:
        rec = gt[0]
        text = gt[1]
        cv2.rectangle(img, tuple(rec[:2]),tuple(rec[2:]), (255, 100, 100), 1  )
        # cv2.putText(img,
        #             text,
        #             tuple(rec[:2]),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),2 )
    return Image.fromarray(img)



def load_dataset_path(root) :
    '''
    从数据集根目录下获取所有图像文件和json文件的文件名并输出
    :param root:
    :return:
    '''
    join = os.path.join
    jpathes = glob.glob(join( root, "jsons", "*.json" ))
    imgpathes = [ j.replace("jsons", "images").replace(".json", ".bmp") for j in jpathes ]
    imgpathes = [ i if os.path.exists(i) else i.replace(".bmp", ".jpeg") for i in imgpathes ]
    for imgp  in imgpathes:
        assert os.path.exists(imgp) , f"{imgp} not exist"
    return imgpathes, jpathes

def crop_img_according_to_gts(im, gts, ignore_first=False):
    '''
    将图像根据ground truth进行裁剪
    :param im:
    :param gts:
    :param ignore_first:
    :return:
    示例：
        j_path = "/data/houfeng/datasets/ocr/jsons/0--19e79366ef48fa0f4b9bcdfc80dd87fd.json"
        i_path = "/data/houfeng/datasets/ocr/images/0--19e79366ef48fa0f4b9bcdfc80dd87fd.bmp"
        img = cv2.imread(i_path)
        buff = json2gt(j_path)
        crops, locations = crop_img_according_to_gts(img, buff)
        plt.imshow(np.array(crops['2011091405:23'])[0])
        plt.show()
    '''
    crops = {}
    locations = {}

    # print(im.shape)
    if ignore_first:
        gts = gts[1:]
    for gt in gts:
        loc, text = gt
        left, top, right, bottom = tuple(loc)
        # img = im[top:bottom + 1, left:right + 1]
        # print(img)
        if text in crops:
            crops[text].append(im[top:bottom+1, left:right+1])
            locations[text].append(loc)
        else:
            crops[text] = [im[top:bottom+1, left:right+1]]
            locations[text] = [loc]
    return crops, locations

def get_mask_according_to_gts( orig_img_shape, gts, down_sample_rate=1, spatial_bandwidth_sigma_factor=1/float(5), ignore_first=False):
    '''
    为每一个标签返回一个guassian mask
    :param orig_img_shape:
    :param gts:
    :param down_sample_rate:
    :param spatial_bandwidth_sigma_factor:
    :param ignore_first:
    :return:
    示例：
        j_path = "/data/houfeng/datasets/ocr/jsons/0--19e79366ef48fa0f4b9bcdfc80dd87fd.json"
        i_path = "/data/houfeng/datasets/ocr/images/0--19e79366ef48fa0f4b9bcdfc80dd87fd.bmp"
        img = cv2.imread(i_path)
        buff = json2gt(j_path)
        mask = get_mask_according_to_gts(img.shape, buff)
        plt.imshow(np.array(mask['2011091405:23']))
        plt.show()
    '''
    # Type (...) -> dict([str:np.array])
    masks = {}
    patch_size = np.array( orig_img_shape )/down_sample_rate
    if ignore_first:
        gts = gts[1:]
    for gt in gts:
        loc, text = gt
        left, top, right, bottom = tuple(loc)
        pos = np.array( [left + right, top + bottom] )/2/down_sample_rate
        mask_size = np.array( [right-left, bottom-top] )/down_sample_rate
        #output_sigma = np.sqrt(np.prod(mask_size)) * spatial_bandwidth_sigma_factor
        output_sigma = mask_size * spatial_bandwidth_sigma_factor
        grid_y = np.arange(np.floor(patch_size[0])) - np.floor(pos[1])
        grid_x = np.arange(np.floor(patch_size[1])) - np.floor(pos[0])
        grid_y = grid_y / output_sigma[1] # x , y 方向的sigama大小不一样
        grid_x = grid_x / output_sigma[0]
        rs, cs = np.meshgrid(grid_x, grid_y)
        #y = np.exp(-0.5 / output_sigma ** 2 * (rs ** 2 + cs ** 2))
        y = np.exp(-0.5 * (rs ** 2 + cs ** 2))
        if text in masks:
            masks[text] += y
        else:
            masks[text] = y
    return masks

if __name__ == '__main__':
    j_path = "/data/houfeng/datasets/maanshan_947imgs/jsons/cam2_0001--00381c39455d8b0aed4e0834e28b1f0a.json"
    i_path = "/data/houfeng/datasets/maanshan_947imgs/images/cam2_0001--00381c39455d8b0aed4e0834e28b1f0a.bmp"
    # img = cv2.imread(i_path)
    buff = json2gt_line(j_path)
    # print(buff)
    # draw_path2img(i_path, j_path)
    # imgpathes, jpathes = load_dataset_path('/data/houfeng/datasets/ocr/')
    # crops, locations = crop_img_according_to_gts(img, buff)
    # mask = get_mask_according_to_gts(img.shape, buff)
    # plt.imshow(np.array(crops['hege'])[0])
    # plt.imshow(np.array(mask['hege']), cmap='gray')
    # plt.show()
    # plt.imshow(img)
    # plt.show()
    imp, jsp = load_dataset_path("/data/houfeng/datasets/maanshan_947imgs")
    print(3)
