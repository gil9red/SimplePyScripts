#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re

import config
import common


PATTERN_GET_JIRA = re.compile(r"\[.*?\] \((\w+?-\d+?)\)")


def get_jira(msg):
    """
    '[.ii] (OPTT-113) . Refactoring' -> 'OPTT-113'

    """

    if not msg:
        return

    match = PATTERN_GET_JIRA.search(msg)
    if match:
        return match.group(1)


log_list = common.get_log_list(config.SVN_FILE_NAME)
# OR:
# log_list = common.get_log_list(config.URL_SVN)

print("Total commits:", len(log_list))


month_by_jira_info = dict()

for log in reversed(log_list):
    jira = get_jira(log.msg)
    if not jira:
        continue

    key = log.date.strftime("%Y/%m")

    if key not in month_by_jira_info:
        month_by_jira_info[key] = set()

    month_by_jira_info[key].add(jira)

for month, jira_items in month_by_jira_info.items():
    # Хитрая сортировка по двум параметрами: имя проекта и номер джиры
    jira_items = sorted(
        jira_items, key=lambda x: (x.split("-")[0], int(x.split("-")[1]))
    )

    print("{}: ({})\t{}".format(month, len(jira_items), jira_items))
