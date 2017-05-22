#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import glob
for file_name in glob.glob('img/*.txt'):
    import imghdr
    img_type = imghdr.what(file_name)
    print('{} -> {}'.format(file_name, img_type))
