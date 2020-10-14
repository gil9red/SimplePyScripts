#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import zipfile
import sys

from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from human_byte_size import sizeof_fmt


FILE_NAME = Path('Doc_df7c89c378c04e8daf69257ea95d9a2e.zip')

print('Zip size:', sizeof_fmt(len(FILE_NAME.read_bytes())))


with zipfile.ZipFile('Doc_df7c89c378c04e8daf69257ea95d9a2e.zip') as f:
    data_file = f.read('Doc_df7c89c378c04e8daf69257ea95d9a2e.html')
    size = sizeof_fmt(len(data_file))
    print(f'File size: {size}')
    print(f'data_file[:100]: {data_file[:100]}')
