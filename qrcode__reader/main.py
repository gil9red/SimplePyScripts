#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import io
from urllib.request import urlopen

import requests

# SOURCE: https://github.com/tomerfiliba/reedsolomon/blob/master/reedsolo.py
# pip install reedsolo
#
# pip install git+https://github.com/ewino/qreader.git
import qreader


# FROM FILE
data = qreader.read("../qrcode__generate/qr_code_1.png")
print(data)  # Hello World!


# FROM URL
url = "https://upload.wikimedia.org/wikipedia/commons/8/8f/Qr-2.png"
data = qreader.read(urlopen(url))
print(data)  # "Version 2"

url = "https://upload.wikimedia.org/wikipedia/commons/e/eb/QR-%D0%BA%D0%BE%D0%B4.png"
data = qreader.read(urlopen(url))
print(data)  # http://ru.wikipedia.org/wiki/QR_Code


# FROM URL as bytes in file-like object
rs = requests.get(url)
image_data = rs.content

bytes_io = io.BytesIO(image_data)

data = qreader.read(bytes_io)
print(data)  # http://ru.wikipedia.org/wiki/QR_Code
