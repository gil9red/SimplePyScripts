#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from urllib.request import urlopen


def get_my_public_ip() -> str:
    with urlopen("https://api.ipify.org/?format=text") as f:
        return f.read().decode("utf-8")


if __name__ == "__main__":
    ip = get_my_public_ip()
    print(f"My IP: {ip}")
