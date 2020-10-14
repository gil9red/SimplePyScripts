#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
import sys

from pathlib import Path

# pip install tqdm
from tqdm import tqdm

# pip install requests
import requests

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from human_byte_size import sizeof_fmt


url = 'https://github.com/gil9red/NotesManager/raw/master/bin.rar'
# Streaming, so we can iterate over the response.
rs = requests.get(url, stream=True)

# Total size in bytes.
total_size = int(rs.headers.get('content-length', 0))
print('From content-length:', sizeof_fmt(total_size))

chunk_size = 1024
num_bars = int(total_size / chunk_size)

file_name = os.path.basename(url)

with open(file_name, mode='wb') as f:
    for data in tqdm(rs.iter_content(chunk_size), total=num_bars, unit='KB', file=sys.stdout):
        f.write(data)

# Read from file
file_data = open(file_name, mode='rb').read()
print('File data size:', sizeof_fmt(len(file_data)))
