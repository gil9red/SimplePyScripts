#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re

# pip install nltk
import nltk


text = """\
Согласен.
В первое ПОЕ
Да вся вторая часть
А читеры — подлецы.
"""

sentences = []
for line in text.splitlines():
    sentences += nltk.sent_tokenize(line, language="russian")

print(*map(repr, sentences))
# 'Согласен.' 'В первое ПОЕ' 'Да вся вторая часть' 'А читеры — подлецы.'

print("-" * 100)

text = text.replace("\n", ". ")
text = re.sub("[.]{2,}", ".", text)

sentences = nltk.sent_tokenize(text, language="russian")
print(*map(repr, sentences))
# 'Согласен.' 'В первое ПОЕ.' 'Да вся вторая часть.' 'А читеры — подлецы.'
