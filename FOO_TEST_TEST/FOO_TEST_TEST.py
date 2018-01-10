#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# import pyautogui
# im1 = pyautogui.screenshot()
# im2 = pyautogui.screenshot('my_screenshot.png')

import cv2

img = cv2.imread('img.png')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imshow('image', gray)
# cv2.waitKey()
# cv2.destroyAllWindows()

# ret, thresh = cv2.threshold(gray, 176, 176, 176)
ret, thresh = cv2.threshold(gray, 176, 176, cv2.THRESH_BINARY)
image, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.imshow('image', image)
cv2.waitKey()
cv2.destroyAllWindows()

# print(sorted([cv2.contourArea(i) for i in contours], reverse=True)[:10])
# contours = [i for i in contours if (cv2.contourArea(i) > 250000 and cv2.contourArea(i) < 255000) or (cv2.contourArea(i) > 11000 and cv2.contourArea(i) < 12000)]

contours = [i for i in contours if 250000 < cv2.contourArea(i) < 255000]

# contours = [i for i in contours if cv2.contourArea(i) > 11000]
print([cv2.contourArea(i) for i in contours])

# print(contours)
# print(hierarchy)
img = cv2.drawContours(img, contours, -1, (0, 255, 0), 3)


cv2.imshow('image', img)
cv2.waitKey()
cv2.destroyAllWindows()
