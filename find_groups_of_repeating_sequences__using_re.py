#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re


def get_groups_seqs(text):
    return [m.group() for m in re.finditer(r"(.)\1+", text)]


if __name__ == "__main__":
    text = "hhhrrrraaavvvvvvv"
    items = get_groups_seqs(text)
    print(items)  # ['hhh', 'rrrr', 'aaa', 'vvvvvvv']
