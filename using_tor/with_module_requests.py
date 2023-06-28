#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# NOTE: tor должен быть запущен
# pip install -U requests[socks]
import requests


proxies = {
    "http": "socks5://localhost:9050",
    "https": "socks5://localhost:9050",
}
url = "http://httpbin.org/ip"
print(requests.get(url, proxies=proxies).text)
