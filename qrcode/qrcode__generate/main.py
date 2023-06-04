#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/lincolnloop/python-qrcode


# In memory
import io

# pip install qrcode
import qrcode


text = "Hello World!"

img = qrcode.make(text)
io_data = io.BytesIO()
img.save(io_data, "png")
data = io_data.getvalue()
print(data)

# In file
img.save("qr_code_1.png")
#
# In file, version 2:
with open("qr_code_2.png", "wb") as f:
    f.write(data)
