#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install nltk
import nltk


text = "Ай да А.С. Пушкин! Ай да сукин сын!"

sentences = nltk.sent_tokenize(text)
print(f"Before ({len(sentences)}): {sentences}")
# Before (3): ['Ай да А.С.', 'Пушкин!', 'Ай да сукин сын!']

sentences = nltk.sent_tokenize(text, language="russian")
print(f"After ({len(sentences)}): {sentences}")
# After (2): ['Ай да А.С. Пушкин!', 'Ай да сукин сын!']
