#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install opencv-python
import cv2


img = cv2.imread("example.jpg")
cv2.imshow("img", img)

# Edges Canny
edges = cv2.Canny(img, 50, 100)
cv2.imshow("Edges Canny", edges)
cv2.imwrite("edges_canny.jpg", edges)

# Edges Canny Invert
edges_invert = cv2.bitwise_not(edges)
cv2.imshow("Edges Canny Invert", edges_invert)
cv2.imwrite("edges_canny_invert.jpg", edges_invert)

cv2.waitKey()
