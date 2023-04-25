#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys


# SOURCE: https://stackoverflow.com/a/1060872/5909792
class mod_call(object):
    def __call__(self, text):
        print(text)


sys.modules[__name__] = mod_call()
