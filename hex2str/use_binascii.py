#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import binascii


def hex2str(hex_string, encoding='utf-8'):
    if isinstance(hex_string, str):
        hex_string = hex_string.encode(encoding)

    return binascii.unhexlify(hex_string).decode(encoding)


def str2hex(text, encoding='utf-8'):
    if isinstance(text, str):
        text = text.encode(encoding)

    return binascii.hexlify(text).decode(encoding).upper()


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
