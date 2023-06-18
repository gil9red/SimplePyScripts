#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from datetime import datetime, timedelta


day_of_year = int(datetime.today().strftime("%j"))
print("day_of_year:", day_of_year)

last_programmer_day = 256 - day_of_year
print("last_programmer_day:", last_programmer_day)

if last_programmer_day >= 0:
    programmer_day = datetime.today() + timedelta(days=last_programmer_day)
    print("\nday of programmer_day:", programmer_day.strftime("%j"))
    print("programmer_day:", programmer_day)

else:
    print("Has already passed")
