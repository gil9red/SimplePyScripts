#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests


# SOURCE: https://stackoverflow.com/a/54585203/5909792
def get_my_public_ip() -> str:
    return requests.get("https://www.wikipedia.org").headers["X-Client-IP"]


if __name__ == "__main__":
    ip = get_my_public_ip()
    print(f"My IP: {ip}")
