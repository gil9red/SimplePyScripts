#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# http://pythonworld.ru/moduli/modul-calendar.html
# https://docs.python.org/3/library/calendar.html
import calendar


a = calendar.HTMLCalendar()

with open("calendar.html", "wb") as f:
    html = a.formatyearpage(2016, width=4)
    f.write(html)
