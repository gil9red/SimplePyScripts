#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path

import requests
from bs4 import BeautifulSoup


DIR = Path(__file__).resolve().parent

DIR_IMAGES = DIR / "images"
DIR_IMAGES.mkdir(parents=True, exist_ok=True)


session = requests.Session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0"


rs = session.get(
    "https://eur.zaful.com/long-sleeve-geometric-lace-dress-puid_2036888.html?kuid=252759"
)
root = BeautifulSoup(rs.content, "html.parser")

for li in root.select("#js-goodsGalleryThumb > ul > li[data-source-img]"):
    url_img = li["data-source-img"]
    print(url_img)

    file_name = url_img.split("/")[-1]

    rs = session.get(url_img)
    (DIR_IMAGES / file_name).write_bytes(rs.content)

"""
https://gloimg.zafcdn.com/zaful/pdm-product-pic/Clothing/2016/12/13/source-img/20161213190242_28449.jpg
https://gloimg.zafcdn.com/zaful/pdm-product-pic/Clothing/2016/12/13/source-img/20161213190242_66497.jpg
https://gloimg.zafcdn.com/zaful/pdm-product-pic/Clothing/2016/12/13/source-img/20161213190243_16127.jpg
https://gloimg.zafcdn.com/zaful/pdm-product-pic/Clothing/2016/12/13/source-img/20161213190243_17500.JPG
https://gloimg.zafcdn.com/zaful/pdm-product-pic/Clothing/2016/12/13/source-img/20161213190243_73427.JPG
"""
