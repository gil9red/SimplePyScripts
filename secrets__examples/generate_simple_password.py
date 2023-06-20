#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://docs.python.org/3/library/secrets.html


import string
from secrets import choice


def generate_password(length=8) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(choice(alphabet) for _ in range(length))


if __name__ == "__main__":
    print(generate_password())
    print(generate_password())
    print()

    for i in (8, 8, 16, 32):
        password = generate_password(length=i)
        print(f"[{len(password)}]: {password}")
