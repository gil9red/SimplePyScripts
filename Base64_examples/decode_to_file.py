#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from base64 import b64decode

# Hello World!
text = 'SGVsbG8gV29ybGQh'

with open('result.txt', 'wb') as f:
    f.write(b64decode(text))
