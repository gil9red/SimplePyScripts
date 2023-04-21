#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
import sys

from datetime import datetime
from logging.handlers import RotatingFileHandler

import cv2
import numpy as np


def get_logger(name, file="log.txt", encoding="utf-8", log_stdout=True, log_file=True):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s"
    )

    if log_file:
        fh = RotatingFileHandler(
            file, maxBytes=10000000, backupCount=5, encoding=encoding
        )
        fh.setFormatter(formatter)
        log.addHandler(fh)

    if log_stdout:
        sh = logging.StreamHandler(stream=sys.stdout)
        sh.setFormatter(formatter)
        log.addHandler(sh)

    return log


def get_current_datetime_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H%M%S.%f")


def find_contours(image_source_hsv, hsv_min, hsv_max):
    thresholded_image = image_source_hsv

    # Отфильтровываем только то, что нужно, по диапазону цветов
    thresholded_image = cv2.inRange(
        thresholded_image,
        np.array(hsv_min, np.uint8),
        np.array(hsv_max, np.uint8)
    )

    # Убираем шум
    thresholded_image = cv2.erode(
        thresholded_image,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    )
    thresholded_image = cv2.dilate(
        thresholded_image,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    )

    # Замыкаем оставшиеся крупные объекты
    thresholded_image = cv2.dilate(
        thresholded_image,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    )
    thresholded_image = cv2.erode(
        thresholded_image,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    )

    # Находим контуры
    contours, _ = cv2.findContours(
        thresholded_image,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    return contours


def find_rect_contours(image_source_hsv, hsv_min, hsv_max):
    return [
        cv2.boundingRect(c)
        for c in find_contours(image_source_hsv, hsv_min, hsv_max)
    ]
