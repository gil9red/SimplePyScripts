#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "IPETRASH"


import re
import string


def remove_punctuation(text):
    pattern = re.compile("[%s]" % re.escape(string.punctuation))
    return pattern.sub("", text)


if __name__ == "__main__":
    text = "classes, freq = defaultdict(lambda:0), defaultdict(lambda:0)"
    print(remove_punctuation(text))
    # classes freq  defaultdictlambda0 defaultdictlambda0
