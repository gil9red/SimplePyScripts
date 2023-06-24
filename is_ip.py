#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re


# SOURCE: https://stackoverflow.com/a/23166561/5909792
IP_RANGE = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"
IP_REGEXP = f"^{IP_RANGE}\.{IP_RANGE}\.{IP_RANGE}\.{IP_RANGE}$"


def is_ip(ip: str) -> bool:
    return bool(re.match(IP_REGEXP, ip))


if __name__ == "__main__":
    tests = [
        ("127.0.0.1", True),
        ("100.100.100.100", True),
        ("0.0.0.0", True),
        ("300.300.300.300", False),
        ("300.0.0.1", False),
        ("255.255.255.255", True),
    ]

    for ip, expected in tests:
        actual = is_ip(ip)
        print(ip, actual)
        assert actual is expected
