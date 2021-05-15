#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
from pathlib import Path


DIR = Path(__file__).resolve().parent
TOKEN_FILE_NAME = DIR / 'TOKEN.txt'

# SOURCE: https://developers.giphy.com/dashboard/
GIPHY_API_KEY = os.environ.get('TOKEN') or TOKEN_FILE_NAME.read_text('utf-8').strip()
