#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install opencv-python
import cv2


img = cv2.imread("example.jpg")
cv2.imshow("img", img)

# Gray
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow("img_gray", img_gray)

img_2 = cv2.imread("example.jpg", cv2.IMREAD_GRAYSCALE)
cv2.imshow("img_gray_2", img_2)

cv2.waitKey()
