# -*- coding: utf-8 -*-

import cv2
# 输出路径
videoPath = 'output_video.mp4'
# 表示视频流格式
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# 20表示输出视频每秒20帧， （295, 295）表示输出的视频的尺寸
videoPathTmp = 'E:\\temp\output'
videoWriter = cv2.VideoWriter(videoPath, fourcc, 15, (295, 295))
for i in range(1000):
    framePath = videoPathTmp + '\\' + str(i) + '.jpg'
    frame = cv2.imread(framePath)
    videoWriter.write(frame)
