#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import pyautogui

# pip install opencv-python
import cv2

import numpy


pil_image = pyautogui.screenshot(region=(200, 200, 200, 200))
print(pil_image.size)
pil_image.show("pil_image")

opencv_image = cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2BGR)
print(opencv_image.shape[:2])

cv2.imshow("opencv_image", opencv_image)
cv2.waitKey()
