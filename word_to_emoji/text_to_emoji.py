#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import re
from typing import List

# pip install pymorphy2
import pymorphy2
from pymorphy2.tokenizers import simple_word_tokenize

from word_to_emoji import db


morph = pymorphy2.MorphAnalyzer()


def get_tokens(text: str, ignore_punctuations=False) -> List[pymorphy2.analyzer.Parse]:
    tokens = [morph.parse(word)[0] for word in simple_word_tokenize(text)]
    if ignore_punctuations:
        tokens = [token for token in tokens if 'PNCT' not in token.tag]
    return tokens


def text_to_emoji(text: str) -> str:
    for token in set(get_tokens(text, ignore_punctuations=True)):
        word = token.word
        emoji = db.Word2Emoji.get_emoji(word)
        if emoji:
            text = re.sub(rf'\b{re.escape(word)}\b', emoji, text, flags=re.IGNORECASE)

    return text


if __name__ == '__main__':
    text = text_to_emoji('Смотри в оба глаза')
    print(text)
    print(repr(text))

    print()

    text = 'xxx: у мальчиков есть воображаемые друзья, а у девочек - воображаемый жыр )))'
    text = text_to_emoji(text)
    print(text)

    print(text_to_emoji('Собака хочет есть'))
