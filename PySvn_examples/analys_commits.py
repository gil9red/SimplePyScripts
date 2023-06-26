#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import config
from common import get_log_list, get_log_list_by_author


url = config.SVN_FILE_NAME

log_list = get_log_list(url)
print(f"Total commits ({len(log_list)}):")

author_by_log = get_log_list_by_author(url, log_list)

for author, logs in sorted(
    author_by_log.items(), key=lambda item: len(item[1]), reverse=True
):
    print(f"    {author}: {len(logs)}")
