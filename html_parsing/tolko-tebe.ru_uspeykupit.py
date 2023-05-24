#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from urllib.parse import urljoin

import requests


def wait(
    days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0
):
    from datetime import timedelta, datetime
    from itertools import cycle
    import sys
    import time

    try:
        progress_bar = cycle("|/-\\|/-\\")

        today = datetime.today()
        timeout_date = today + timedelta(
            days=days,
            seconds=seconds,
            microseconds=microseconds,
            milliseconds=milliseconds,
            minutes=minutes,
            hours=hours,
            weeks=weeks,
        )

        def str_timedelta(td: timedelta) -> str:
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
            print("[{}] Time left to wait: {}".format(next(progress_bar), left), end="")
            sys.stdout.flush()

            # Delay 1 seconds
            time.sleep(1)

            today = datetime.today()

        print("\r" + " " * 100 + "\r", end="")

    except KeyboardInterrupt:
        print()
        print("Waiting canceled")


session = requests.session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"

session.get("https://tolko-tebe.ru/")


headers = {
    "X-Requested-With": "XMLHttpRequest",
}

while True:
    rs = session.post("https://tolko-tebe.ru/uspeykupit", headers=headers)
    data = rs.json()

    title = data["title"]

    price = data["price"]
    price_action = data["price_action"]

    mins = data["mins"]
    secs = data["secs"]
    time_left = f"{mins}:{secs}"

    url_product = urljoin(rs.url, "/product/" + data["path"])
    print(
        f"{title!r}\n"
        f"    Цена {price} ₽, со скидкой {price_action} ₽\n"
        f"    {url_product}\n"
        f"    Осталось: {time_left}\n"
        # f"    raw_data: {data}\n"
    )

    wait(minutes=mins, seconds=secs)

# OUTPUT example:
# 'SKINLITE Очищающая маска, стягивающая поры'
#     Цена 385 ₽, со скидкой 193 ₽
#     https://tolko-tebe.ru/product/skinlite-ochischayuschaya-maska-styagivayuschaya-pory
#     Осталось: 12:47
