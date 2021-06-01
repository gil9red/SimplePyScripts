#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
import sys

from pathlib import Path
from typing import Optional


DIR = Path(__file__).resolve().parent

# NOTE: хак для помощи импортирования из telegram_notifications
sys.path.append(str(DIR.parent))

TOKEN_PATH = DIR / 'TOKEN.txt'
TOKEN = os.environ.get('TOKEN') or TOKEN_PATH.read_text('utf-8').strip()

CHAT_ID_PATH = DIR / 'CHAT_ID.txt'
CHAT_ID: Optional[int] = None
try:
    CHAT_ID = int(
        os.environ.get('CHAT_ID') or CHAT_ID_PATH.read_text('utf-8').strip()
    )
except:
    pass

ERROR_TEXT = 'Возникла какая-то проблема. Попробуйте повторить запрос или попробовать чуть позже...'
