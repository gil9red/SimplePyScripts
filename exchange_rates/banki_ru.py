#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests


def exchange_rate(currency_id, timestamp=None):
    if timestamp is None:
        from datetime import datetime

        timestamp = int(datetime.today().timestamp())

    data = {
        "currency_id": currency_id,
        "date": timestampб
    }

    headers = {
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
    }

    rs = requests.post(
        "http://www.banki.ru/products/currency/ajax/quotations/value/cbr/",
        json=data,
        headers=headers,
    )
    return rs.json()["value"]


if __name__ == "__main__":
    # 840 -- USD
    print("USD:", exchange_rate(840))

    # 978 -- EUR
    print("EUR:", exchange_rate(978))
