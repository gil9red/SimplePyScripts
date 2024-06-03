#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def from_ghbdtn(text: str) -> str:
    en = """qwertyuiop[]asdfghjkl;'zxcvbnm,./`QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~"""
    ru = """йцукенгшщзхъфывапролджэячсмитьбю.ёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё"""

    translator = dict(zip(en, ru))
    table = str.maketrans(translator)

    return text.translate(table)


if __name__ == "__main__":
    text = "B ,skb ghj,ktvs c ujcntdjq dhjlt ,s? gjcvjnhb "
    print(text)
    print(from_ghbdtn(text))
    assert from_ghbdtn(text) == "И были проблемы с гостевой вроде бы, посмотри "

    assert from_ghbdtn("Привет! Ghbdtn! Hello!") == "Привет! Привет! Руддщ!"
