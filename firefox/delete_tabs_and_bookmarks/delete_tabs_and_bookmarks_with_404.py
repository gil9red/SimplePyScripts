#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
import sys
import time

from pathlib import Path

import requests

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))

import api
from common import get_logger
from config import file_name_places, file_name_session


log = get_logger(__file__, DIR / "logs")


def is_404(
    url: str,
    log: logging.Logger,
) -> bool:
    while True:
        try:
            rs = requests.get(url)
            return rs.status_code == 404
        except Exception as e:
            log.error(f"Error {str(e)!r} on {url}")
            return False  # Skip url
        finally:
            time.sleep(2)


log.info("Start")

tab_urls = api.get_tab_urls(file_name_session)
log.info(f"Tab urls: {len(tab_urls)}")

bookmark_urls = api.get_bookmark_urls(file_name_places)
log.info(f"Bookmark urls: {len(bookmark_urls)}")

urls = set(tab_urls + bookmark_urls)
count = len(urls)
log.info(f"Urls to processing: {count}")

for i, url in enumerate(urls, 1):
    # Every 10%
    if i % (count // 10) == 0:
        log.info(f"Processed {i / count:.0%}")

    if not is_404(url, log):
        continue

    api.close_tabs(file_name_session, [url], log)
    api.close_bookmarks(file_name_places, [url], log)

log.info("Finish")
