#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))

import api
from common import get_logger
from config import file_name_places, file_name_session


log = get_logger(__file__, DIR / 'logs')

log.info('Start')

tab_urls = api.get_tab_urls(file_name_session)
log.info(f'Tab urls: {len(tab_urls)}')

bookmark_urls = api.get_bookmark_urls(file_name_places)
log.info(f'Bookmark urls: {len(bookmark_urls)}')

api.close_tabs(file_name_session, bookmark_urls, log)

log.info('Finish')
