#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
from urllib.request import urlopen


def get_my_public_ip() -> str:
    with urlopen("https://httpbin.org/get") as f:
        return json.loads(f.read())["origin"]


if __name__ == "__main__":
    ip = get_my_public_ip()
    print(f"My IP: {ip}")
