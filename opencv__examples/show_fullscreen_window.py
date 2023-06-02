#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import cv2


window_name = "window"
img = cv2.imread("gaussian_blur/example.jpg")

while True:
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    cv2.imshow(window_name, img)

    if cv2.waitKey(25) == 27:  # Esc to quit
        sys.exit()
