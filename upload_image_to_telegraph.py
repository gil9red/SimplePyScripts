#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import mimetypes
import os

from urllib.parse import urljoin

import requests


def upload_image_to_telegraph(file_name_or_url: str) -> str:
    user_agent = (
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0"
    )
    headers = {
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Referer": "https://telegra.ph/",
        "User-Agent": user_agent,
    }

    if os.path.exists(file_name_or_url):
        img = open(file_name_or_url, "rb")
        mime = mimetypes.guess_type(file_name_or_url)[0]

    else:
        rs = requests.get(file_name_or_url, headers={"User-Agent": user_agent})
        img = rs.content
        mime = rs.headers["Content-Type"]

    files = {"file": ("blob", img, mime)}
    rs = requests.post("http://telegra.ph/upload", files=files, headers=headers)

    img_url = urljoin("http://telegra.ph/", rs.json()[0]["src"])
    return img_url


if __name__ == "__main__":
    import traceback

    urls = [
        # Local file name:
        "Visa Test System screenshot communication s8|ettings.png",
        # Urls:
        "https://qph.ec.quoracdn.net/main-qimg-6c945d3d82f6a2d261f45c17099a799f-c",
        "http://newspaper.readthedocs.io/en/latest/_static/newspaper.jpg",
    ]

    for url in urls:
        try:
            url_image = upload_image_to_telegraph(url)
            print(f"{url} -> {url_image}")

        except Exception as e:
            print(f"{url} -> {e}\n\n{traceback.format_exc()}")
