#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import codecs


def rot13(message):
    return codecs.encode(message, "rot13")


if __name__ == '__main__':
    assert rot13("test") == "grfg"
    assert rot13("Test") == "Grfg"
