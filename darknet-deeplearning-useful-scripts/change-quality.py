#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import glob

# pip install opencv-python
import cv2
import numpy


def rescale_frame(frame, shape: tuple, percent=50) -> numpy.ndarray:
    width = int(shape[1] * percent / 100)
    height = int(shape[0] * percent / 100)
    dim = width, height
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)


for f in glob.glob("*.png"):
    frame = cv2.imread(f)
    shape = frame.shape
    frame = cv2.UMat(frame)
    frame = rescale_frame(frame, shape, 20)
    frame = rescale_frame(frame, shape, 100)
    cv2.imwrite(f, frame, [int(cv2.IMWRITE_PNG_COMPRESSION), 30])
