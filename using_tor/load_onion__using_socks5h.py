#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# About socks5h:
# https://stackoverflow.com/a/43823166/5909792
# "It's important to specify the proxies using the socks5h:// scheme so that DNS resolution
# is handled over SOCKS so Tor can resolve the .onion address properly."
#
# https://github.com/urllib3/urllib3/issues/1035

# NOTE: tor должен быть запущен
# pip install -U requests[socks]
import requests


# Порт может быть и 9050, и 9150, и возможно другой. Нужно смотреть настройки tor. Например, tor можно через
# Tor Browser запускать, в настройках сети Tor браузера будет указан порт tor
proxies = {
    "http": "socks5h://127.0.0.1:9050",
    "https": "socks5h://127.0.0.1:9050",
}

data = requests.get("http://altaddresswcxlld.onion/", proxies=proxies).content
print(data)

data = requests.get("https://www.facebookcorewwwi.onion/", proxies=proxies).content
print(data)

data = requests.get("http://sblib3fk2gryb46d.onion/", proxies=proxies).content
print(data)
