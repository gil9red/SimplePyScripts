#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install opencv-python
import cv2

import numpy as np


def find_contours(image_source_hsv, hsv_min, hsv_max):
    thresholded_image = image_source_hsv

    # Отфильтровываем только то, что нужно, по диапазону цветов
    thresholded_image = cv2.inRange(
        thresholded_image, np.array(hsv_min, np.uint8), np.array(hsv_max, np.uint8)
    )

    # Убираем шум
    thresholded_image = cv2.erode(
        thresholded_image, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    )
    thresholded_image = cv2.dilate(
        thresholded_image, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    )

    # Замыкаем оставшиеся крупные объекты
    thresholded_image = cv2.dilate(
        thresholded_image, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    )
    thresholded_image = cv2.erode(
        thresholded_image, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    )

    # Находим контуры
    contours, _ = cv2.findContours(
        thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    return contours


def draw_rect_contours(img, hsv_min, hsv_max):
    img = img.copy()

    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    contours = find_contours(img_hsv, hsv_min, hsv_max)

    for contour in contours:
        rect = cv2.boundingRect(contour)
        x, y, w, h = rect

        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 4)

    return img


img = cv2.imread("example.jpg")
cv2.imshow("img", img)

# Find yellow
img_yellow = draw_rect_contours(img, hsv_min=(25, 113, 220), hsv_max=(66, 255, 255))
cv2.imshow("img_yellow", img_yellow)

# Find green
img_green = draw_rect_contours(img, hsv_min=(59, 128, 130), hsv_max=(99, 255, 255))
cv2.imshow("img_green", img_green)

# Find red
img_red = draw_rect_contours(img, hsv_min=(119, 159, 184), hsv_max=(179, 255, 255))
cv2.imshow("img_red", img_red)

cv2.waitKey()
cv2.destroyAllWindows()
