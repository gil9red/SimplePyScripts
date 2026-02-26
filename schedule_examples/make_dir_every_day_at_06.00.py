#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
import os

from datetime import date


def job() -> None:
    print(date.today())

    try:
        os.mkdir(r"T:\ipetrash")

    except FileExistsError:
        pass


if __name__ == "__main__":
    # pip install schedule
    import schedule

    schedule.every().day.at("6:00").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
