#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# import pyautogui
# im1 = pyautogui.screenshot()
# im2 = pyautogui.screenshot('my_screenshot.png')


import numpy as np

import cv2
img = cv2.imread('img.png')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imshow('image', gray)
# cv2.waitKey()
# cv2.destroyAllWindows()

# ret, thresh = cv2.threshold(gray, 176, 176, 176)
ret, thresh = cv2.threshold(gray, 176, 176, cv2.THRESH_BINARY)
image, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# cv2.imshow('image', image)
# cv2.waitKey()
# cv2.destroyAllWindows()

# print(sorted([cv2.contourArea(i) for i in contours], reverse=True)[:10])
# contours = [i for i in contours if (cv2.contourArea(i) > 250000 and cv2.contourArea(i) < 255000) or (cv2.contourArea(i) > 11000 and cv2.contourArea(i) < 12000)]

contours = [i for i in contours if 250000 < cv2.contourArea(i) < 255000]

# board_frame = contours[0]
# print(board_frame)
# quit()

# contours = [i for i in contours if cv2.contourArea(i) > 11000]
# print([cv2.contourArea(i) for i in contours])

# print(contours)
# print(hierarchy)
# mask = np.zeros_like(img)
# cv2.drawContours(mask, contours, 0, (0, 255, 0), 3)
img_with_contour = img.copy()
cv2.drawContours(img_with_contour, contours, -1, (0, 255, 0), 3)

rect_board = cv2.boundingRect(contours[0])
# rect_board = cv2.boundingRect(np.array(0,0, 0,0, 200,0, 200,0))
# print(rect_board)
x, y, h, w = rect_board

# cv2.imshow('img_with_contour', img_with_contour)
# cv2.imshow('image', img)
# cv2.imshow('gray', gray)

crop_img = img[y:y+h, x:x+w]
cv2.imshow("cropped", crop_img)


# crop_img[crop_img == 255] = [0, 0, 255]
gray_crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
gray_crop_img[gray_crop_img == 176] = 0

cv2.imshow("gray_crop_img", gray_crop_img)

ret, thresh = cv2.threshold(gray_crop_img, 100, 255, cv2.THRESH_BINARY)

gray_crop_img_Contours, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# print([cv2.contourArea(i) for i in contours])
cell_contours = [i for i in contours if 11000 < cv2.contourArea(i) < 12000]

copy_crop_img = crop_img.copy()
cv2.drawContours(copy_crop_img, contours, -1, (0, 255, 0), 3)
cv2.imshow("all_cropped_contours", copy_crop_img)

cv2.drawContours(crop_img, cell_contours, -1, (0, 255, 0), 3)
cv2.imshow("cropped_contours", crop_img)
cv2.imshow("gray_crop_img_Contours", gray_crop_img_Contours)


cv2.waitKey()
cv2.destroyAllWindows()
