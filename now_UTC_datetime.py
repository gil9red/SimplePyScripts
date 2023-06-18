#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as DT


utc_datetime = DT.datetime.utcnow()
print(utc_datetime.strftime("%d/%m/%Y %H:%M:%S"))
