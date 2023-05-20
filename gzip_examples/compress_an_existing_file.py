#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import gzip
import shutil


file_name = __file__

with open(file_name, "rb") as f_in:
    with gzip.open(file_name + ".gz", "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
