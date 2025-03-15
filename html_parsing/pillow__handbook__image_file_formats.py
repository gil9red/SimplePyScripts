#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup


def get_formats(css_selector: str) -> list[str]:
    return [el["id"] for el in root.select(f"{css_selector} > section[id]")]


rs = requests.get(
    "https://pillow.readthedocs.io/en/latest/handbook/image-file-formats.html"
)
root = BeautifulSoup(rs.content, "html.parser")

fully_supported_formats = get_formats("#fully-supported-formats")
print(fully_supported_formats)
# ['blp', 'bmp', 'dds', 'dib', 'eps', 'gif', 'icns', 'ico', 'im', 'jpeg',
# 'jpeg-2000', 'mpo', 'msp', 'pcx', 'pfm', 'png', 'ppm', 'sgi', 'spider',
# 'tga', 'tiff', 'webp', 'xbm']

read_only_formats = get_formats("#read-only-formats")
print(read_only_formats)
# ['cur', 'dcx', 'fits', 'fli-flc', 'fpx', 'ftex', 'gbr', 'gd', 'imt',
# 'iptc-naa', 'mcidas', 'mic', 'pcd', 'pixar', 'psd', 'qoi', 'sun', 'wal',
# 'wmf-emf', 'xpm']

write_only_formats = get_formats("#write-only-formats")
print(write_only_formats)
# ['palm', 'pdf', 'xv-thumbnails']
