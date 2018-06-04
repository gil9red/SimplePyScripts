#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install git+https://github.com/ewino/qreader.git
# pip install reedsolo
import qreader


# From FILE
data = qreader.read('../qrcode__generate/qr_code_1.png')
print(data)  # prints "Version 2"


# From URL
url = 'https://upload.wikimedia.org/wikipedia/commons/8/8f/Qr-2.png'
from urllib.request import urlopen
data = qreader.read(urlopen(url))
print(data)  # prints "Version 2"


# From URL as bytes in file-like object
import requests
rs = requests.get(url)
image_data = rs.content  # bytes

import io
bytes_io = io.BytesIO(image_data)

data = qreader.read(bytes_io)
print(data)  # prints "Version 2"
