#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
from pathlib import Path


DIR = Path(__file__).resolve().parent


API_HASH_FILE_NAME = DIR / "API_HASH.txt"
API_ID_FILE_NAME = DIR / "API_ID.txt"

API_HASH = os.environ.get("API_HASH") or API_HASH_FILE_NAME.read_text("utf-8").strip()
API_ID = os.environ.get("API_ID") or API_ID_FILE_NAME.read_text("utf-8").strip()
