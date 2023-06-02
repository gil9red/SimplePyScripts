#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import pathlib


file_name = "C:/Users/111/video.mp4"
path = pathlib.Path(file_name)
print(path.name)  # video.mp4
print(path.stem)  # video

print()

file_name = "video.mp4"
path = pathlib.Path(file_name)
print(path.name)  # video.mp4
print(path.stem)  # video
