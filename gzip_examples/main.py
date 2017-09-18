#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import gzip

# From file name
with gzip.open('build-kernel.xml.gz') as f:
    file_content = f.read()
    print(file_content)


# From bytes / memory file
bytes_data = open('build-kernel.xml.gz', mode='rb').read()

import io
byte_io = io.BytesIO(bytes_data)

with gzip.open(byte_io) as f:
    file_content = f.read()
    print(file_content)


# From url as bytes / memory file
from urllib.request import urlopen
with urlopen('http://httpbin.org/gzip') as rs:
    bytes_data = rs.read()
    byte_io = io.BytesIO(bytes_data)

    with gzip.open(byte_io) as f:
        file_content = f.read()
        print(file_content)
