#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from bs4 import BeautifulSoup
import requests


def get_formats(css_selector: str) -> list:
    formats_els = (
        root.select_one(css_selector)
        .find_next_sibling("ul")
        .find_all("li", recursive=False)
    )
    return [li.a.get_text(strip=True) for li in formats_els]


rs = requests.get(
    "https://pillow.readthedocs.io/en/latest/handbook/image-file-formats.html"
)
root = BeautifulSoup(rs.content, "html.parser")

fully_supported_formats = get_formats('#contents a[href="#fully-supported-formats"]')
print(fully_supported_formats)
# ['BMP', 'DIB', 'EPS', 'GIF', 'ICNS', 'ICO', 'IM', 'JPEG', 'JPEG 2000',
# 'MSP', 'PCX', 'PNG', 'PPM', 'SGI', 'SPIDER', 'TGA', 'TIFF', 'WebP', 'XBM']

read_only_formats = get_formats('#contents a[href="#read-only-formats"]')
print(read_only_formats)
# ['BLP', 'CUR', 'DCX', 'DDS', 'FLI, FLC', 'FPX', 'FTEX', 'GBR', 'GD',
# 'IMT', 'IPTC/NAA', 'MCIDAS', 'MIC', 'MPO', 'PCD', 'PIXAR', 'PSD', 'WAL',
# 'WMF', 'XPM']

write_only_formats = get_formats('#contents a[href="#write-only-formats"]')
print(write_only_formats)
# ['PALM', 'PDF', 'XV Thumbnails']
