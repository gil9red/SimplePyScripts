#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time

import config
from common import get_log_list


url = config.URL_SVN

last_log = get_log_list(url, limit=1)[0]
last_revision = last_log.revision
print(
    f'Start from commit rev{last_revision} by {last_log.author}: "{repr(last_log.msg)}" in {last_log.date}'
)

while True:
    log_list = get_log_list(url, revision_from=last_revision)
    if len(log_list) > 1:
        # Первым в списке будет коммит с ревизией revision_from
        log_list = log_list[1:]

        last_log = log_list[-1]

        if last_revision != last_log.revision:
            print(
                f'commits +{len(log_list)} from: rev{last_revision} by {last_log.author}: '
                f'"{repr(last_log.msg)}" in {last_log.date}....{log_list}\n'
            )

            last_revision = last_log.revision

    # Every 10 minutes
    time.sleep(60 * 10)
