#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import gzip
import shutil

from urllib.request import urlopen


# 241.8 MB
url = "http://discogs-data.s3-us-west-2.amazonaws.com/data/2018/discogs_20180201_artists.xml.gz"
in_file_name = url.split("/")[-1]
out_file_name = in_file_name[:-3]

# Download -> decompress and save in out_file_name
with gzip.open(urlopen(url)) as f_in:
    with open(out_file_name, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
