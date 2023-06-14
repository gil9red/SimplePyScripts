#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re


def find_longest(s):
    return max(re.findall(r"((\w+?)\2+)", s), key=lambda t: t[0].count(t[1]))


if __name__ == "__main__":
    text = "helloworld world world hellohellohelloworldworld"
    print(find_longest(text))  # ('hellohellohello', 'hello')
