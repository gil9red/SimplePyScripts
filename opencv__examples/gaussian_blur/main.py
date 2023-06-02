#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install opencv-python
import cv2


img = cv2.imread("example.jpg")
cv2.imshow("img", img)

img_blur = cv2.GaussianBlur(img, (5, 5), 0)
cv2.imshow("img_blur", img_blur)

cv2.waitKey()
