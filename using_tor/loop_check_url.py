#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
import sys
import time

# pip install -U requests[socks]
import requests


proxies = {
    "http": "socks5://localhost:9050",
    "https": "socks5://localhost:9050",
}

# NOTE: Для смены ip нужно настроить tor
# Для этого создается torrc файл (\Data\Tor\torrc)
# И в него добавляется содержимое:
# NewCircuitPeriod 5
# MaxCircuitDirtiness 10

url = "http://httpbin.org/ip"

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("[%(asctime)s] %(message)s"))
log.addHandler(handler)

while True:
    try:
        log.debug(requests.get(url, proxies=proxies).json())
    except requests.exceptions.ConnectionError:
        log.debug("WARN: Not found Tor")

    time.sleep(1)
