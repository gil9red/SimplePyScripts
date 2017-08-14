#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def hex2str(hex_string):
    items = list()

    for i in range(0, len(hex_string), 2):
        hex2 = hex_string[i] + hex_string[i + 1]
        char = chr(int(hex2, 16))
        items.append(char)

    return ''.join(items)


def str2hex(text):
    items = list()

    for c in text:
        # 'P' -> 0x50 -> 50
        hex_char = hex(ord(c))[2:].upper()
        items.append(hex_char)

    return ''.join(items)


if __name__ == '__main__':
    assert hex2str("504F53542068747470733A") == "POST https:"
    assert str2hex(hex2str("504F53542068747470733A")) == "504F53542068747470733A"
    assert str2hex("POST https:") == "504F53542068747470733A"
    assert hex2str(str2hex("POST https:")) == "POST https:"

    hex_text = "504F53542068747470733A"
    text = hex2str(hex_text)
    print('"{}"'.format(text))

    text = "POST https:"
    hex_text = str2hex(text)
    print(hex_text)
