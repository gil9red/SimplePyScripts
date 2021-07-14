#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def from_ghbdtn(text: str) -> str:
    # SOURCE: https://ru.stackoverflow.com/a/812203/201445
    layout = dict(zip(map(ord, '''qwertyuiop[]asdfghjkl;'zxcvbnm,./`QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'''),
                               '''йцукенгшщзхъфывапролджэячсмитьбю.ёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'''))

    return text.translate(layout)


if __name__ == '__main__':
    text = 'B ,skb ghj,ktvs c ujcntdjq dhjlt ,s? gjcvjnhb '
    print(text)
    print(from_ghbdtn(text))
    assert from_ghbdtn(text) == 'И были проблемы с гостевой вроде бы, посмотри '
