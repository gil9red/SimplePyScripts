#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from datetime import datetime

# pip install schedule
import schedule


schedule.every().hour.do(print, "every hour")
schedule.every(8).hours.do(print, "every 8 hour")
schedule.every().saturday.at("00:00").do(print, "every saturday at 00:00")
schedule.every().day.at("12:00").do(print, "every day at 12:00")

print(datetime.now())
for job in schedule.jobs:
    print(f"{job}, next run: {job.next_run}")
"""
2024-05-20 11:50:26.588010
Job(interval=1, unit=hours, do=print, args=('every hour',), kwargs={}), next run: 2024-05-20 12:50:26.588010
Job(interval=8, unit=hours, do=print, args=('every 8 hour',), kwargs={}), next run: 2024-05-20 19:50:26.588010
Job(interval=1, unit=weeks, do=print, args=('every saturday at 00:00',), kwargs={}), next run: 2024-05-25 00:00:00
Job(interval=1, unit=days, do=print, args=('every day at 12:00',), kwargs={}), next run: 2024-05-20 12:00:00
"""
