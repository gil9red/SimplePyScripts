#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install Pillow
from PIL import Image


image = Image.open("input.jpg")
width, height = image.size

ROW_COUNT = 3
COLUMN_COUNT = 5

grid_image = Image.new(
    "RGB",
    (width * COLUMN_COUNT, height * ROW_COUNT),
    (255, 255, 255),
)

for row in range(ROW_COUNT):
    y = row * width

    for column in range(COLUMN_COUNT):
        x = column * height
        grid_image.paste(image, (x, y))

grid_image.show()
grid_image.save("output.jpg")
