#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт рисует на видео в правом нижнем углу указанный текст.

"""


# http://ffmpeg.org/ffmpeg-filters.html#drawtext-1


import os
from subprocess import Popen, PIPE


command_pattern = (
    """ffmpeg -i {in} """
    """-vf drawtext="fontfile={font}: text='{text}': """
    """fontcolor={text_color}: fontsize={fontsize}: x={x}: y={y}" """
    """-vb 20M {out} """
)

params = {
    "in": "BH_Logo.wmv",
    "out": "BH_Logo_new.wmv",
    "text": "http://ffmpeg.org/ffmpeg-filters.html#drawtext-1",
    "font": "FreeSerif.ttf",
    "fontsize": 30,
    "text_color": "white",
    # Рисование в правом нижнем угле с небольшим отступом от границ
    "x": "w - text_w - 5",
    "y": "h - text_h - 5",
}

# Экранирование ":" (двоеточие), т.к. оно является символом разделение параметров
# команды фильтра
params["text"] = params["text"].replace(":", "\\:")

command = command_pattern.format(**params)
print(command)

if os.path.exists(params["out"]):
    os.remove(params["out"])

with Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True) as process:
    out, err = process.communicate()
    print(out)
    print("-" * 25)
    print(err)

print("-" * 25)
print("{} size: {}".format(params["in"], os.path.getsize(params["in"])))
print("{} size: {}".format(params["out"], os.path.getsize(params["out"])))
