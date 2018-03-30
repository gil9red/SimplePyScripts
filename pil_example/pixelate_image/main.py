#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://gist.github.com/danyshaanan/6754465

"""
A Python script to pixelate an image and add a thin black margin between the simulated pixels.

"""

from PIL import Image

background_color = (0, 0, 0)  # black
pixel_size = 9

image = Image.open('input.jpg')
image = image.resize((image.size[0] // pixel_size, image.size[1] // pixel_size), Image.NEAREST)
image = image.resize((image.size[0] * pixel_size, image.size[1] * pixel_size), Image.NEAREST)
pixel = image.load()

image.save('output_without_margin.jpg')
image.show()

# Draw black margin between pixels
for i in range(0, image.size[0], pixel_size):
    for j in range(0, image.size[1], pixel_size):
        for r in range(pixel_size):
            pixel[i+r, j] = background_color
            pixel[i, j+r] = background_color

image.save('output.jpg')
image.show()
