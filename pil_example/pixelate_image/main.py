#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://gist.github.com/danyshaanan/6754465

"""
A Python script to pixelate an image and add a thin black margin between the simulated pixels.

"""

from PIL import Image


def pixelate(image, pixel_size=9, draw_margin=True):
    margin_color = (0, 0, 0)

    image = image.resize((image.size[0] // pixel_size, image.size[1] // pixel_size), Image.NEAREST)
    image = image.resize((image.size[0] * pixel_size, image.size[1] * pixel_size), Image.NEAREST)
    pixel = image.load()

    # Draw black margin between pixels
    if draw_margin:
        for i in range(0, image.size[0], pixel_size):
            for j in range(0, image.size[1], pixel_size):
                for r in range(pixel_size):
                    pixel[i+r, j] = margin_color
                    pixel[i, j+r] = margin_color

    return image


if __name__ == '__main__':
    image = Image.open('input.jpg')

    image_pixelate = pixelate(image, draw_margin=False)
    image_pixelate.save('output_without_margin.jpg')
    image_pixelate.show()

    image_pixelate = pixelate(image)
    image_pixelate.save('output.jpg')
    image_pixelate.show()
