#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def rot13(message):
    import codecs
    return codecs.encode(message, 'rot13')


assert rot13("test") == "grfg"
assert rot13("Test") == "Grfg"
