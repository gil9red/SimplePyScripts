#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# import pyautogui
# im1 = pyautogui.screenshot()
# im2 = pyautogui.screenshot('my_screenshot.png')


import numpy as np

import cv2
# img = cv2.imread('img.png')
img = cv2.imread('img_bad.png')
cv2.imshow('img', img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('gray', gray)

# ret, thresh = cv2.threshold(gray, 176, 176, 176)
ret, thresh = cv2.threshold(gray, 176, 176, cv2.THRESH_BINARY)
image, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.imshow('image_', image)
# cv2.waitKey()
# cv2.destroyAllWindows()

# print(sorted([cv2.contourArea(i) for i in contours], reverse=True)[:10])
# contours = [i for i in contours if (cv2.contourArea(i) > 250000 and cv2.contourArea(i) < 255000) or (cv2.contourArea(i) > 11000 and cv2.contourArea(i) < 12000)]

contours = [i for i in contours if 250000 < cv2.contourArea(i) < 255000]
print([cv2.contourArea(i) for i in contours])
print([cv2.contourArea(i) for i in contours if 250000 < cv2.contourArea(i) < 255000])


cv2.waitKey()
cv2.destroyAllWindows()

quit()

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

cv2.imshow('img_with_contour', img_with_contour)
# cv2.imshow('image', img)
# cv2.imshow('gray', gray)


rect_board = cv2.boundingRect(contours[-1])
# rect_board = cv2.boundingRect(np.array(0,0, 0,0, 200,0, 200,0))
# print(rect_board)
x, y, h, w = rect_board
crop_img = img[y:y+h, x:x+w]
# cv2.imshow("cropped", crop_img)


# crop_img[crop_img == 255] = [0, 0, 255]
gray_crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

# Для помощи алгоритма контурирования изменим цвет пикселей сетки на черный
gray_crop_img[gray_crop_img == 176] = 0

# cv2.imshow("gray_crop_img", gray_crop_img)

ret, thresh = cv2.threshold(gray_crop_img, 100, 255, cv2.THRESH_BINARY)
# print(ret, thresh)

gray_crop_img_Contours, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# cv2.imshow("gray_crop_img_Contours", gray_crop_img_Contours)
# print([cv2.contourArea(i) for i in contours])
cell_contours = [i for i in contours if 11000 < cv2.contourArea(i) < 12000]

i = 1
print(len(cell_contours))  # 16
print([(cv2.boundingRect(contour)[0], cv2.boundingRect(contour)[1]) for contour in cell_contours])

# matrix_cell_contours = []


sort_x = sorted([cv2.boundingRect(x)[0] for x in cell_contours])
mean_of_points = [
    sum(sort_x[0:4]) // 4,
    sum(sort_x[4:8]) // 4,
    sum(sort_x[8:12]) // 4,
    sum(sort_x[12:16]) // 4,
]

# print(mean_of_points)
MEAN_EPS = 5
# print(sorted([cv2.boundingRect(x)[1] for x in cell_contours]))

point_by_contour = dict()
for contour in cell_contours:
    x, y, _, _ = cv2.boundingRect(contour)
    # print(x, y)

    for mean_point in mean_of_points:

        # Максимальное отклонение от средней позиции
        if abs(x - mean_point) <= MEAN_EPS:
            x = mean_point

        if abs(y - mean_point) <= MEAN_EPS:
            y = mean_point

    # print(x, y)
    # print()

    point_by_contour[(x, y)] = contour

# print(sorted([cv2.boundingRect(x)[1] for x in cell_contours]))

# print(list(sorted(point_by_contour.keys())))
# quit()

# from collections import defaultdict
# x_by_contour = defaultdict(list)
# y_by_contour = defaultdict(list)
# for contour in cell_contours:
#     x, y, _, _ = cv2.boundingRect(contour)
#     x_by_contour[x].append(contour)
#     y_by_contour[y].append(contour)

# print(x_by_contour)
# print(y_by_contour)

# for y, coutour_list in sorted(y_by_contour.items(), key=lambda x: x[0]):
#     coutour_list.sort(key=lambda x: cv2.boundingRect(x)[0])
#
#     matrix_cell_contours += coutour_list

cell_contours.sort(key=lambda x: (cv2.boundingRect(x)[1], cv2.boundingRect(x)[0]))
# cell_contours.sort(key=lambda x: cv2.boundingRect(x)[:2])
# cell_contours.sort(key=lambda x: (cv2.boundingRect(x)[1], -cv2.boundingRect(x)[0]))
# import operator
# cell_contours.sort(key=lambda x: operator.itemgetter(1, 2)(x[:2]))
print([(cv2.boundingRect(contour)[0], cv2.boundingRect(contour)[1]) for contour in cell_contours])

# matrix_cell_contours = [
#     cell_contours[0:4],
#     cell_contours[4:7],
#     cell_contours[7:10],
#     cell_contours[10:11],
# ]

# xx = cell_contours
#
# matrix_cell_contours = []
# matrix_cell_contours += cell_contours[0:4]
# matrix_cell_contours += cell_contours[4:8]
# matrix_cell_contours += cell_contours[8:12]
# matrix_cell_contours += cell_contours[12:16]

# for contour in cell_contours:
for pos, contour in sorted(point_by_contour.items(), key=lambda x: (x[0][1], x[0][0])):
    rect_cell = cv2.boundingRect(contour)
    x, y, w, h = rect_cell
    x, y = pos

    cv2.putText(crop_img, str(i), (x, y + h//4), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0, 0, 0))
    cv2.putText(crop_img, '{}x{}'.format(x, y), (x, y + h // 2), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.5, (0, 0, 0))

    # x, y = pos
    # cv2.putText(crop_img, '{}x{}'.format(x, y), (x, y + h // 2), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.5, (0, 0, 0))
    i += 1

cv2.drawContours(crop_img, cell_contours, -1, (0, 255, 0), 3)
cv2.imshow("cropped_cell_contours", crop_img)

# copy_crop_img = crop_img.copy()
# cv2.drawContours(copy_crop_img, contours, -1, (0, 255, 0), 3)
# cv2.imshow("all_cropped_contours", copy_crop_img)

cv2.waitKey()
cv2.destroyAllWindows()
