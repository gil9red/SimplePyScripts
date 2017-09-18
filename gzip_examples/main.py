#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import gzip

# From file name
with gzip.open('build-kernel.xml.gz') as f:
    file_content = f.read()
    print(repr(file_content))

# From bytes
import io
byte_io = io.BytesIO(open('build-kernel.xml.gz', mode='rb').read())

with gzip.open(byte_io) as f:
    file_content = f.read()
    print(repr(file_content))
