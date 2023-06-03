#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
from pathlib import Path


DIR = Path(__file__).resolve().parent
TOKEN_FILE_NAME = DIR / "TOKEN.txt"

TOKEN = os.environ.get("TOKEN") or TOKEN_FILE_NAME.read_text("utf-8").strip()

# http://user:password@proxy_host:proxy_port
PROXY = None

if PROXY:
    os.environ["http_proxy"] = PROXY
