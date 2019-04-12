# -*- coding: utf-8 -*-
__author__ = 'ghostlyfeng'
__time__ = '2018/12/1 19:45'

import numpy as np
from PIL import Image

path="E:\datasets\英雄联盟\data_test\data_test_set_cluster_0.npz"
data=np.load(path)
x_train=data["images"]
y_train=data["boxes"]
print(len(y_train))
for i in range(2):
    print(x_train[i])
    im = Image.fromarray(x_train[i])
    im.show()