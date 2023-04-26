#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Вытаскивание и сохранение на диск файлов логотипов

"""

import base64
import os

from bs4 import BeautifulSoup


FILE_NAME_DICT_LOGO = "mini_full_dict__CONTACT/logo.xml"

DIR_LOGO_IMAGES = "logo_images"
os.makedirs(DIR_LOGO_IMAGES, exist_ok=True)

root = BeautifulSoup(open(FILE_NAME_DICT_LOGO, "rb"), "lxml")

for row in root.select("rowdata > row"):
    logo_name = row["logo_name"]
    print(logo_name)

    logo_data = row["logo_data"]
    img_data = base64.b64decode(logo_data)

    file_name = os.path.join(DIR_LOGO_IMAGES, logo_name)

    with open(file_name, "wb") as f:
        f.write(img_data)
