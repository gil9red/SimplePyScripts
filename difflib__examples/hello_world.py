#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import difflib


words = [
    'смыло', 'соло', 'вяло', 'мяло', 'смола', 'поле', 'воля', 'с мола', 'была',
    'стела', 'с мела', 'смело'
]
word = 'смело'

print(difflib.get_close_matches(word, words))              # ['смело', 'смыло', 'с мела']
print(difflib.get_close_matches(word, words, cutoff=0.6))  # ['смело', 'смыло', 'с мела']
print(difflib.get_close_matches(word, words, cutoff=0.8))  # ['смело', 'смыло']
