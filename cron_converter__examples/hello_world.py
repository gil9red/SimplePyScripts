#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from datetime import datetime

# pip install cron-converter
from cron_converter import Cron


print("Every hour")
cron = "0 * * * *"
cron_instance = Cron(cron)

print(f"Cron: {cron_instance}")

start_date = datetime.now()
print(f"Start date: {start_date}")

schedule = cron_instance.schedule(start_date)
print(f"Next: {schedule.next().isoformat()}")
print(f"Next: {schedule.next().isoformat()}")
print(f"Next: {schedule.next().isoformat()}")

print()

print("Every 8 hours")
cron = "0 */8 * * *"
cron_instance = Cron(cron)

print(f"Cron: {cron_instance}")

start_date = datetime.now()
print(f"Start date: {start_date}")

schedule = cron_instance.schedule(start_date)
print(f"Next: {schedule.next().isoformat()}")
print(f"Next: {schedule.next().isoformat()}")
print(f"Next: {schedule.next().isoformat()}")

print()

print("Every 00:00")
cron = "0 0 * * *"
cron_instance = Cron(cron)

print(f"Cron: {cron_instance}")

start_date = datetime.now()
print(f"Start date: {start_date}")

schedule = cron_instance.schedule(start_date)
print(f"Next: {schedule.next().isoformat()}")
print(f"Next: {schedule.next().isoformat()}")
print(f"Next: {schedule.next().isoformat()}")

print()

print("Every 00:00 at Saturday")
cron = "0 0 * * 6"
cron_instance = Cron(cron)

print(f"Cron: {cron_instance}")

start_date = datetime.now()
print(f"Start date: {start_date}")

schedule = cron_instance.schedule(start_date)
print(f"Next: {schedule.next().isoformat()}")
print(f"Next: {schedule.next().isoformat()}")
print(f"Next: {schedule.next().isoformat()}")
