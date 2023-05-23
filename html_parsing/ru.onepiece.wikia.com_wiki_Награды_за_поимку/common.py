#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
import re

import requests


FILE_NAME = "Награды_за_поимку.html"


def get_html() -> bytes:
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "rb") as f:
            html = f.read()
    else:
        rs = requests.get("http://ru.onepiece.wikia.com/wiki/Награды_за_поимку")
        html = rs.content

        with open(FILE_NAME, "wb") as f:
            f.write(html)

    return html


def process_td(td) -> str:
    text = td.text.strip()
    text = re.sub(r"\[\d+\]", "", text)
    text = re.sub(r"\s{2,}", " ", text)

    text = " / ".join(map(str.strip, text.split("/")))
    return text
