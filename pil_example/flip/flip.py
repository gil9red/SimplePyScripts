#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


if __name__ == '__main__':
    from PIL import Image
    from PIL.ImageOps import flip

    im = Image.open('im.png')
    im = flip(im)
    im.show()
