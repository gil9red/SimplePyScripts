#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
from pathlib import Path


DIR = Path(__file__).resolve().parent
TOKEN_FILE_NAME = DIR / "TOKEN.txt"

TOKEN = os.environ.get("TOKEN") or TOKEN_FILE_NAME.read_text("utf-8").strip()

ERROR_TEXT = "⚠ Возникла какая-то проблема. Попробуйте повторить запрос или попробовать чуть позже..."
