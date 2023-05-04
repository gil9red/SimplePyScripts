#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import glob
import imghdr

for file_name in glob.glob("img/*.txt"):
    img_type = imghdr.what(file_name)
    print("{} -> {}".format(file_name, img_type))
