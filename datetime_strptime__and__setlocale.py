#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT
import locale


def check():
    try:
        print(DT.datetime.strptime("Fri, 06-Nov-2020 21:36:45 GMT", "%a, %d-%b-%Y %H:%M:%S %Z"))
    except Exception as e:
        print(f'[-] {e}')


check()
# 2020-11-06 21:36:45

locale.setlocale(locale.LC_TIME, 'ru')
check()
# [-] time data 'Fri, 06-Nov-2020 21:36:45 GMT' does not match format '%a, %d-%b-%Y %H:%M:%S %Z'

locale.setlocale(locale.LC_TIME, 'C')
check()
# 2020-11-06 21:36:45
