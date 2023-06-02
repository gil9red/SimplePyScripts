#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install opencv-python
import cv2


img = cv2.imread("example.jpg")
# cv2.imshow('img', img)

img_data = cv2.imencode(".jpg", img)[1].tostring()
print(len(img_data), img_data)
