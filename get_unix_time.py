#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime
import time


def get_unix_time() -> int:
    d = datetime.datetime.now()
    unix_time = int(time.mktime(d.timetuple()))
    return unix_time


if __name__ == '__main__':
    unix_time = get_unix_time()
    print(unix_time)

    # print()
    #
    # while True:
    #     print(get_unix_time())
    #     time.sleep(1)
