#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import Optional, List
from difflib import SequenceMatcher

# pip install pymorphy2
import pymorphy2
from pymorphy2.tokenizers import simple_word_tokenize

morph = pymorphy2.MorphAnalyzer()


def get_tokens(text: str) -> List[pymorphy2.analyzer.Parse]:
    return [morph.parse(word)[0] for word in simple_word_tokenize(text)]


ALL_WORDS = ['замена', 'заменить', 'касса']


def fix_command(word: str) -> Optional[str]:
    rations = [
        (word2, SequenceMatcher(None, word, word2).ratio())
        for word2 in ALL_WORDS
    ]
    rations = [(word, ratio) for word, ratio in rations if ratio >= 0.7]
    if not rations:
        return

    return max(rations, key=lambda x: x[1])[0]


commands = [
    'замена кассы',
    'заменить кассs',
    'замени кассу',
]
for command in commands:
    words = get_tokens(command)
    norm_words = [fix_command(word.normal_form) for word in words]
    print(command, norm_words)
