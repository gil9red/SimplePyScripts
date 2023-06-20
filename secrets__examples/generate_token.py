#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://docs.python.org/3/library/secrets.html


from secrets import token_bytes, token_hex


if __name__ == "__main__":
    for i in (None, 8, 8, 16, 32):
        token = token_bytes() if i is None else token_bytes(i)
        print(f"[{len(token)}]: {token}")

    print()

    for i in (None, 8, 8, 16, 32):
        token = token_hex() if i is None else token_hex(i)
        print(f"[{len(token)}]: {token}")
