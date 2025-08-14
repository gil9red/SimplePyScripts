#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from datetime import date, timedelta


day_of_year: int = int(date.today().strftime("%j"))
print(f"Current day of year: {day_of_year}")

last_programmer_day: int = 256 - day_of_year
print(f"Until Programmer's day: {last_programmer_day}")

if last_programmer_day >= 0:
    programmer_day = date.today() + timedelta(days=last_programmer_day)
    print()
    print(f"Day of programmer day: {programmer_day:%j}")
    print(f"Programmer day: {programmer_day}")
else:
    print("Has already passed")
