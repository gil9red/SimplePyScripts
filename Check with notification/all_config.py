#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
from pathlib import Path


DIR = Path(__file__).resolve().parent

SMS_TOKEN_FILE_NAME = DIR / 'SMS_TOKEN.txt'
SMS_TOKEN = os.environ.get('SMS_TOKEN') or SMS_TOKEN_FILE_NAME.read_text('utf-8').strip()

# <API_ID>:<PHONE>
API_ID, TO = SMS_TOKEN.split(':')
