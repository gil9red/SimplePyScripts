#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import gzip
import shutil


in_file_name = "build-kernel.xml.gz"
out_file_name = in_file_name[:-3]

with gzip.open(in_file_name) as f_in:
    with open(out_file_name, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
