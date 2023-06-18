#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import hashlib


def get_password_hash(name: str, password: str) -> str:
    if not name:
        raise ValueError('"name" is empty!')

    if not password:
        raise ValueError('"password" is empty!')

    data = (name.upper() + "-" + password).encode("UTF-8")
    return hashlib.sha256(data).hexdigest().upper()


if __name__ == "__main__":
    print(get_password_hash("abc", "123"))
    assert (
        get_password_hash("abc", "123")
        == "4D156D7BC9C38C000AA1E5B06E46E1F40CAFE651F3CABFAE9BAD48803BAF17BF"
    )

    print(get_password_hash("123", "abc"))
    assert (
        get_password_hash("123", "abc")
        == "84A990F85C3CDD4A5FE71B027996AF81E3F87062BE029FAC4C09DDC40B3C42F0"
    )
