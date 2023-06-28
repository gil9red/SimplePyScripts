#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from datetime import datetime


utc_datetime = datetime.utcnow()
print(utc_datetime.strftime("%d/%m/%Y %H:%M:%S"))
