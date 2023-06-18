#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def upper_print(f):
    def wrapper(*args, **kwargs):
        f(*[i.upper() if hasattr(i, "upper") else i for i in args], **kwargs)

    return wrapper


if __name__ == "__main__":
    text = "hello world!"

    print(text)  # hello world!

    old_print = print
    print = upper_print(print)

    print(text)  # HELLO WORLD!

    print = old_print
    print(text)  # hello world!
