#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from datetime import datetime


week_number = datetime.now().isocalendar()[1]
print("week_number:", week_number)
