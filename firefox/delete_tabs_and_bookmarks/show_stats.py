#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))

import api
from config import file_name_places, file_name_session


tab_urls = api.get_tab_urls(file_name_session)
print(f"Tab urls: {len(tab_urls)}")

bookmark_urls = api.get_bookmark_urls(file_name_places)
print(f"Bookmark urls: {len(bookmark_urls)}")