#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from pathlib import Path

# pip install chardet
import chardet


DIR = Path(__file__).resolve().parent


for path in DIR.glob('*.txt'):
    raw_data = path.read_bytes()
    print(path.name, chardet.detect(raw_data))

# ascii.txt {'encoding': 'ascii', 'confidence': 1.0, 'language': ''}
# cp1251.txt {'encoding': 'windows-1251', 'confidence': 0.99, 'language': 'Russian'}
# utf-8.txt {'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}
