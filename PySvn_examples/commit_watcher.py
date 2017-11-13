#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import config
url = config.URL_SVN

from common import get_log_list
last_log = get_log_list(url, limit=1)[0]
last_revision = last_log.revision
print('Start from commit rev{} by {}: "{}" in {}'.format(
    last_revision,
    last_log.author,
    repr(last_log.msg),
    last_log.date
))

while True:
    log_list = get_log_list(url, revision_from=last_revision)
    if len(log_list) > 1:
        # Первым в списке будет коммит с ревизией revision_from
        log_list = log_list[1:]

        last_log = log_list[-1]

        if last_revision != last_log.revision:
            print('commits +{} from: rev{} by {}: "{}" in {}....{}\n'.format(
                len(log_list),
                last_revision,
                last_log.author,
                repr(last_log.msg),
                last_log.date,
                log_list
            ))

            last_revision = last_log.revision

    # Every 10 minutes
    import time
    time.sleep(60 * 10)
