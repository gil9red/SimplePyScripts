#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re


def get_groups_seqs(text):
    return [match[0] for match in re.finditer(r"(.)\1+", text)]


if __name__ == "__main__":
    text = "acccabcfbbffffffcccc"
    items = get_groups_seqs(text)
    print(items)  # ['ccc', 'bb', 'ffffff', 'cccc']
