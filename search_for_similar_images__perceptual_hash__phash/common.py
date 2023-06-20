#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
from pathlib import Path

from PyQt5.QtCore import QStandardPaths

# For import: shorten and sizeof_fmt
sys.path.append("../")
from explore__windows import explore
from human_byte_size import sizeof_fmt
from shorten import shorten


# def fill_html_table(key_values: dict) -> str:
#     html_table = '<table border="0" cellspacing="5" cellpadding="0">'
#
#     for k, v in key_values.items():
#         html_table += f'<tr><td align="left"><b>{k}:</b></td><td align="left">{v}</td></tr>'
#
#     html_table += '</table>'
#     return html_table


DIR_IMAGES = str(Path(__file__).resolve().parent / "images")

IMAGE_HASH_ALGO = [
    "average_hash",
    "phash",
    "phash_simple",
    "dhash",
    "dhash_vertical",
    "whash",
    "colorhash",
]
DEFAULT_IMAGE_HASH_ALGO = "phash"
DEFAULT_IMAGE_HASH_MAX_SCORE = 10

DEFAULT_SUFFIXES = "jpg,jpeg,png,bmp"

USER_PICTURES_DIR = QStandardPaths.standardLocations(QStandardPaths.PicturesLocation)[0]

ICON_WIDTH = 128
ICON_HEIGHT = 128

SETTINGS_FILE_NAME = "settings.ini"
