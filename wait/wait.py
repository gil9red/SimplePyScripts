#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as DT
import sys
import time

from itertools import cycle


def wait(
    days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0
):
    try:
        progress_bar = cycle(("|", "/", "-", "\\"))

        today = DT.datetime.today()
        timeout_date = today + DT.timedelta(
            days=days,
            seconds=seconds,
            microseconds=microseconds,
            milliseconds=milliseconds,
            minutes=minutes,
            hours=hours,
            weeks=weeks,
        )

        def str_timedelta(td: DT.timedelta) -> str:
            td = str(td)

            # Remove ms
            # 0:01:40.123000 -> 0:01:40
            if "." in td:
                td = td[: td.rindex(".")]

            # 0:01:40 -> 00:01:40
            if td.startswith("0:"):
                td = "00:" + td[2:]

            return td

        while today <= timeout_date:
            left = timeout_date - today
            left = str_timedelta(left)

            print("\r" + " " * 100 + "\r", end="")
            print(f"[{next(progress_bar)}] Time left to wait: {left}", end="")
            sys.stdout.flush()

            # Delay 1 seconds
            time.sleep(1)

            today = DT.datetime.today()

        print("\r" + " " * 100 + "\r", end="")

    except KeyboardInterrupt:
        print()
        print("Waiting canceled")


if __name__ == "__main__":
    wait(seconds=1)
    wait(seconds=3)
    wait(seconds=5)

    print("Start wait")
    wait(seconds=1)
    print("Finish wait")

    while True:
        print()
        print("Current datetime:", DT.datetime.now())
        print()
        wait(minutes=1, seconds=30)
