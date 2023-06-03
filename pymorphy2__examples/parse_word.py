#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install pymorphy2
import pymorphy2


morph = pymorphy2.MorphAnalyzer()

words = ["Думала", "Подумала", "Согласен"]

for word in words:
    print(repr(word))

    parsed_word = morph.parse(word)[0]
    print(parsed_word.tag)
    print()

# 'Думала'
# VERB,impf,intr femn,sing,past,indc
#
# 'Подумала'
# VERB,perf,intr femn,sing,past,indc
#
# 'Согласен'
# ADJS,Qual masc,sing
