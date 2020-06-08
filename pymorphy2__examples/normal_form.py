#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install pymorphy2
import pymorphy2
morph = pymorphy2.MorphAnalyzer()


def get_normal_form(word):
    return morph.parse(word)[0].normal_form


print(get_normal_form('Иванова'))  # иванов
print(get_normal_form('Иванов'))   # иванов
