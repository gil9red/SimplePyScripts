#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from itertools import groupby


def get_groups_seqs(text):
    return ["".join(v) for _, v in groupby(text)]


if __name__ == "__main__":
    text = "hhhrrrraaavvvvvvv"
    items = get_groups_seqs(text)
    print(items)  # ['hhh', 'rrrr', 'aaa', 'vvvvvvv']
