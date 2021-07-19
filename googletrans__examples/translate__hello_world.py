#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install translate
from translate import Translator


translator = Translator(to_lang="ru")
translation = translator.translate("This is a pen.")
print(translation)
assert translation == 'Это ручка.'

translator = Translator(from_lang="ru", to_lang='en')
translation = translator.translate("Привет мир!")
print(translation)
assert translation == 'Hello World!'
