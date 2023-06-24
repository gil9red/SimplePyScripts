#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import ipaddress


def is_valid_ip(ip) -> bool:
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False


if __name__ == "__main__":
    assert is_valid_ip("127.0.0.1") is True
    assert is_valid_ip("255.255.255.255") is True
    assert is_valid_ip("127.0.0.0.1") is False
    assert is_valid_ip("127.0.0.0.-1") is False
