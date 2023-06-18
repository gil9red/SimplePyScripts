#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
import requests


def md5decryption(hash_):
    form_data = {"hash": hash_, "submit": "Decrypt It!"}
    rs = requests.post("http://www.md5decryption.com/", data=form_data)

    match = re.search("Decrypted Text:(.+)", rs.text)

    # Если не нашли
    if not match:
        return

    text = match.group(1)

    # Выцепляем ответ (пример "</b>kombat</font>")
    match = re.search("</b>(.+?)</font>", text)
    if match:
        return match.group(1)

    return text


if __name__ == "__main__":
    print(md5decryption("45af13298a22119fa84debdfc6b2d909"))  # kombat
    print(md5decryption("ed076287532e86365e841e92bfc50d8c"))  # Hello World!
