#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install nltk
import nltk

# pip install pymorphy2
import pymorphy2
from pymorphy2.shapes import is_punctuation


morph = pymorphy2.MorphAnalyzer()

text = """\
Согласен. В первое ПОЕ не было озвучено 80% диалогов, зато взамен мы получили офигенно написаную книгу. Там действительно литературный язык, который приятно читать. Что на инлгише, что на русском. А когда озвучиваешь все диалоги в РПГ, то тут, как бы выбор невелик. Время на это и так дофига тратят. Плюс стоит все это недешево. А значит что? Правильно. Диалоги надо сокращать. Вот и получили обрубок шикарных диалогов во второй части.
Да вся вторая часть вообще какое-то недоразумение, имхо. Вот так вот...
А читеры — подлецы.
"""

sentences = nltk.sent_tokenize(text, language="russian")

for sent in sentences:
    print(repr(sent))

    words = nltk.word_tokenize(sent)
    print(f"({len(words)}): {words}")

    words_no_punct = [word for word in words if not is_punctuation(word)]
    print(f"({len(words_no_punct)}): {words_no_punct}")

    words_no_punct = [word for word in words if "PNCT" not in morph.parse(word)[0].tag]
    print(f"({len(words_no_punct)}): {words_no_punct}")
    print()
