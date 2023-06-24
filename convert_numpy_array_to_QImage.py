#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as DT

import numpy as np

from PIL import ImageGrab
from PyQt5.QtGui import qRgb, QImage



GRAY_COLOR_TABLE = [qRgb(i, i, i) for i in range(256)]


def convert_numpy_array_to_QImage(numpy_array):
    if numpy_array.dtype != np.uint8:
        raise Exception("Need np.array with dtype=np.uint8!")

    height, width = numpy_array.shape[:2]

    if len(numpy_array.shape) == 2:
        img = QImage(
            numpy_array.data,
            width,
            height,
            numpy_array.strides[0],
            QImage.Format_Indexed8,
        )
        img.setColorTable(GRAY_COLOR_TABLE)
        return img

    elif len(numpy_array.shape) == 3:
        if numpy_array.shape[2] == 3:
            img = QImage(
                numpy_array.data,
                width,
                height,
                numpy_array.strides[0],
                QImage.Format_RGB888,
            )
            return img

        elif numpy_array.shape[2] == 4:
            img = QImage(
                numpy_array.data,
                width,
                height,
                numpy_array.strides[0],
                QImage.Format_ARGB32,
            )
            return img


if __name__ == "__main__":
    print_screen_pil = ImageGrab.grab()
    width, height = print_screen_pil.size[0], print_screen_pil.size[1]

    print_screen_numpy = np.array(print_screen_pil.getdata(), dtype="uint8")
    print_screen_numpy = print_screen_numpy.reshape((height, width, 3))

    img = convert_numpy_array_to_QImage(print_screen_numpy)
    print(img.size())

    file_name = f"print_screen_{DT.datetime.now():%Y-%m-%d_%H%M%S}.png"
    print(file_name)

    img.save(file_name)
