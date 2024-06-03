#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def swap_keyboard(text: str) -> str:
    en = """qwertyuiop[]asdfghjkl;'zxcvbnm,./`QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~"""
    ru = """йцукенгшщзхъфывапролджэячсмитьбю.ёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё"""

    translator = {**dict(zip(ru, en)), **dict(zip(en, ru))}
    table = str.maketrans(translator)

    return text.translate(table)


if __name__ == "__main__":
    text = "B ,skb ghj,ktvs c ujcntdjq dhjlt ,s? gjcvjnhb "
    print(text)
    print(swap_keyboard(text))
    assert swap_keyboard(text) == "И были проблемы с гостевой вроде бы, посмотри "

    assert swap_keyboard("Ghbdtn! Руддщ!") == "Привет! Hello!"
    assert swap_keyboard("Ghbdtn! 123 Руддщ!") == "Привет! 123 Hello!"

    text = "Ghbdtn! Руддщ!"
    assert swap_keyboard(swap_keyboard(text)) == text
