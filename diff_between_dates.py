#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from datetime import datetime


items = [
    "23/03/2007",
    "05/12/2007",
    "22/08/2008",
    "02/10/2009",
]

for i in range(len(items) - 1):
    date_str_1, date_str_2 = items[i], items[i + 1]

    date_1 = datetime.strptime(date_str_1, "%d/%m/%Y")
    date_2 = datetime.strptime(date_str_2, "%d/%m/%Y")
    days = (date_2 - date_1).days

    print(f"{date_str_1} - {date_str_2} -> {days} days")
