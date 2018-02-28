#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


name_list = ['Константин', 'Виктор', 'Любовь', 'Дамир', 'Венера',
             'Таисия', 'Алёна', 'Евгений', 'Егор', 'Никита']

# pip install pymorphy2
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

for name in name_list:
    parsed_word = morph.parse(name)[0]
    print('{:<15} {}'.format(name, parsed_word.tag.gender))
