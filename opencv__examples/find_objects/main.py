#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install opencv-python
import cv2


img = cv2.imread("image.png")
cv2.imshow("img", img)

gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret, thresh = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY)
# cv2.imshow('thresh', thresh)

contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cv2.imshow('image_', image)

# img_with_contour = img.copy()
# cv2.drawContours(img_with_contour, contours, -1, (0, 255, 0), 3)
# cv2.imshow('img_with_contour', img_with_contour)

img_with_rect = img.copy()

for contour in contours:
    rect = cv2.boundingRect(contour)
    x, y, w, h = rect

    cv2.rectangle(img_with_rect, (x, y), (x + w, y + h), (0, 0, 255))

cv2.imshow("img_with_rect", img_with_rect)

#
# Draw img_with_rect_rect
#
cv2.drawContours(img_with_rect, contours, -1, (0, 255, 0), 10)
gray_img = cv2.cvtColor(img_with_rect, cv2.COLOR_BGR2GRAY)
contours, _ = cv2.findContours(gray_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cv2.imshow('image_', image)

img_with_rect_rect = img.copy()

for contour in contours:
    rect = cv2.boundingRect(contour)
    x, y, w, h = rect

    cv2.rectangle(img_with_rect_rect, (x, y), (x + w, y + h), (0, 0, 255))

cv2.imshow("img_with_rect_rect", img_with_rect_rect)

cv2.waitKey()
cv2.destroyAllWindows()
