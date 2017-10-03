#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return "%3.1f %s" % (num, 'TB')


from tqdm import tqdm
import requests

url = 'https://github.com/gil9red/NotesManager/raw/master/bin.rar'
# Streaming, so we can iterate over the response.
rs = requests.get(url, stream=True)

# Total size in bytes.
total_size = int(rs.headers.get('content-length', 0))
print('From content-length:', sizeof_fmt(total_size))

import io
bytes_buffer = io.BytesIO()

chunk_size = 1024
num_bars = int(total_size / chunk_size)

import sys

for data in tqdm(rs.iter_content(chunk_size), total=num_bars, unit='KB', file=sys.stdout):
    bytes_buffer.write(data)

file_data = bytes_buffer.getvalue()
print('File data size:', sizeof_fmt(len(file_data)))
