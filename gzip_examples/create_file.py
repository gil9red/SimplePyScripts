#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import gzip


content = b"Lots of content here"
with gzip.open("file.txt.gz", "wb") as f:
    f.write(content)
