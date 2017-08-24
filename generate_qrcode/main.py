#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


text = 'Hello World!'

# pip install qrcode
from qrcode import make as make_qrcode
im = make_qrcode(text)

# In memory
import io
io_data = io.BytesIO()
im.save(io_data, 'png')
data = io_data.getvalue()
print(data)

# In file
im.save('qr_code_1.png')
#
# In file, version 2:
with open('qr_code_2.png', 'wb') as f:
    f.write(data)
