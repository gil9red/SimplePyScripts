#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT
import sys

# pip install opencv-python
import cv2
import numpy


def draw_overlay(img: numpy.ndarray, text: str, color_text=(255, 255, 255), max_text_height_percent=5):
    h, w, _ = img.shape

    max_text_height = (h / 100) * max_text_height_percent

    thickness = 1
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 30

    # Подбор масштабирования текста, чтобы вместить его по ширине
    while True:
        (text_rect_w, text_rect_h), _ = cv2.getTextSize(text, font, scale, thickness)
        if text_rect_w <= w and text_rect_h <= max_text_height:
            break

        scale -= 0.1

    # По центру
    text_y = h - text_rect_h // 2

    # cv2.LINE_AA -- Anti aliased line
    cv2.putText(img, text, (0, text_y), font, scale, color_text, thickness, lineType=cv2.LINE_AA)


def draw_overlay_current_datetime(
        img: numpy.ndarray, datetime_fmt='%d/%m/%y %H:%M:%S',
        color_text=(255, 255, 255), max_text_height_percent=5
):
    text = DT.datetime.now().strftime(datetime_fmt)
    draw_overlay(img, text, color_text, max_text_height_percent)


if __name__ == '__main__':
    img = cv2.imread('example.jpg')

    while True:
        img_overlay = img.copy()
        draw_overlay_current_datetime(img_overlay)

        cv2.imshow('With overlay', img_overlay)

        if cv2.waitKey(25) == 27:  # Esc to quit
            sys.exit()
