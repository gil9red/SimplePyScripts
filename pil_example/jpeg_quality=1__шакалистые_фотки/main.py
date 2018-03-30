#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PIL import Image
im = Image.open('input.jpg')
im.save('output.jpg', format='JPEG', quality=1)
