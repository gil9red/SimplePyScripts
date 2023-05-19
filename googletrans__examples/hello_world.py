#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install googletrans
from googletrans import Translator


text = """
At this Time, two great empires struggled for dominion over Ivalice: Archadia in the East, Rozarria, the West.
The Invasion of the Kingdom of Nabradia was Archadia's first Step in its westward March.
"""
from_lang = "en"
to_lang = "ru"

translator = Translator()
translation = translator.translate(
    text,
    src=from_lang,
    dest=to_lang
).text
print(translation)
# В это время две великие империи боролись за власть над Ivalice: Archadia на Востоке, Rozarria, Запада.
# Вторжение Королевства Nabradia был первый шаг Archadia в ее западном направлении марта.
