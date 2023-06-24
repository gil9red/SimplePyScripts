#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
import re

from collections import defaultdict
from datetime import datetime as dt


def parser_my_jira_time_logs(log):
    """
    Функция принимает список строк вида:
    7417 10:00-12:00
    7417 12:19-14:00
    7417 14:37-15:30
    7417 15:58-17:50

    7415 15:58-15:59

    7456 14:28-15:59

    То, что перед ' ' -- уникальный номер задания
    Диапазон после ' ' -- отрезок времени вида: начало - конец

    Далее функция подсчитает количество часов и минут для каждого задания
    и выведет их
    """

    # TODO: Защита от копипаста: строки могут повторяться и время подсчитается неправильно
    # TODO: Если часы перевалят за 24, то начнется отсчет заного
    # TODO: Для джиры дни и недели не астрономические: 1d = 8h и 1w = 5d

    pattern = re.compile(r"(.+) (\d\d:\d\d)-(\d\d:\d\d)")

    jira_time = defaultdict(int)

    for line in log.split("\n"):
        if line:
            m = pattern.match(line.strip())

            jira = m.group(1)
            t1 = m.group(2)
            t2 = m.group(3)
            delta = dt.strptime(t2, "%H:%M") - dt.strptime(t1, "%H:%M")
            seconds = delta.seconds

            jira_time[jira] += seconds

    for jira, secs in jira_time.items():
        t = time.gmtime(secs)
        h = t.tm_hour
        m = t.tm_min
        jira_time = None
        if h:
            jira_time = str(h) + "h"
        if m:
            if jira_time:
                jira_time += " " + str(m) + "m"
            else:
                jira_time = str(m) + "m"

        print("%s: %s" % (jira, jira_time))


parser_my_jira_time_logs(
    """
    7417 10:00-12:00
    7417 12:19-14:00
    7417 14:37-15:30
    7417 15:58-17:50
    
    7415 15:58-15:59
    
    7456 14:28-15:59
    """
)
