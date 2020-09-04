#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def shorten(text: str, length=30) -> str:
    if not text:
        return text

    if len(text) > length:
        text = text[:length] + '...'
    return text


if __name__ == '__main__':
    text = '1234' * 20
    new_text = shorten(text)
    assert new_text == '123412341234123412341234123412...'

    text = '12345'
    new_text = shorten(text, length=5)
    assert new_text == '12345'

    text = '123'
    new_text = shorten(text, length=5)
    assert new_text == '123'

    text = '12356'
    new_text = shorten(text, length=3)
    assert new_text == '123...'
