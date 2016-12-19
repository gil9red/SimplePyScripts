#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def from_ghbdtn(text):
    """ Convert
      "b ,skb ghj,ktvs c ujcntdjq" -> "и были проблемы с гостевой"
      "ghbdtn" -> "привет"
    """

    en_keyboard = 'qwertyuiop[]asdfghjkl;\'\zxcvbnm,./`?'
    ru_keyboard = 'йцукенгшщзхъфывапролджэ\ячсмитьбю.ё,'

    result = ''

    for c in text:
        en_index = en_keyboard.find(c.lower())
        if en_index != -1:
            result += ru_keyboard[en_index]
        else:
            result += c

    return result


if __name__ == '__main__':
    text = 'B ,skb ghj,ktvs c ujcntdjq dhjlt ,s? gjcvjnhb '
    print(text)
    print(from_ghbdtn(text))
