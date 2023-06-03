#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install pymorphy2
import pymorphy2
from pymorphy2.tokenizers import simple_word_tokenize


morph = pymorphy2.MorphAnalyzer()


def get_tokens(text: str, ignore_punctuations=False) -> list[pymorphy2.analyzer.Parse]:
    tokens = [morph.parse(word)[0] for word in simple_word_tokenize(text)]
    if ignore_punctuations:
        tokens = [token for token in tokens if "PNCT" not in token.tag]
    return tokens


if __name__ == "__main__":
    text = "чё за дом! ни конфет, ни печенек, пришлось жрать СОЛЁНЫЙ огурец (("

    for token in get_tokens(text, ignore_punctuations=True):
        print(token.word, token.normal_form)
