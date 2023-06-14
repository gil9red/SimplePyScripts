#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re


def abbreviate(s):
    def _on_match(match):
        word = match.group()
        return word[0] + str(len(word[1:-2])) + word[-1]

    return re.sub(r"\b(\w+)\b", _on_match, s)


text = "elephant-ride colinu"
print(abbreviate(text))  # e5t-r1e c3u
