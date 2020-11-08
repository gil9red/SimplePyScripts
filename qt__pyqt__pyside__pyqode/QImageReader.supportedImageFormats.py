#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtGui import QImageReader

print(
    list(map(lambda x: x.data().decode(), QImageReader.supportedImageFormats()))
)
# ['bmp', 'cur', 'gif', 'icns', 'ico', 'jpeg', 'jpg', 'pbm', 'pgm', 'png', 'ppm', 'svg', 'svgz', 'tga', 'tif', 'tiff', 'wbmp', 'webp', 'xbm', 'xpm']
