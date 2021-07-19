#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import time
import traceback

# pip install translate
from translate import Translator

# pip install goslate
import goslate

from word_to_emoji import db
from html_parsing.emojipedia_org__search import get_emoji


translator = Translator(from_lang="ru", to_lang='en')
gs = goslate.Goslate()


def ru2en(text: str) -> str:
    text_en = translator.translate(text)

    # Если translate перестал работать попробуем через другой перевести
    if 'MYMEMORY WARNING: YOU USED ALL AVAILABLE FREE TRANSLATIONS FOR TODAY' in text_en:
        text_en = gs.translate(text, 'en')

    return text_en


while True:
    for word_ru in reversed(db.Word2Emoji.get_unprocessed_words()):
        # Если эмодзи уже есть
        if db.Word2Emoji.get_emoji(word_ru):
            continue

        while True:
            try:
                # На emojipedia поиск нужен на английском
                word = ru2en(word_ru)
                emoji = get_emoji(word)
                print(f'Add {word_ru!r} ({word!r}) -> {emoji!r}')
                if not emoji:
                    continue

                db.Word2Emoji.add(word_ru, emoji)
                break

            except:
                print(traceback.format_exc())
                time.sleep(5 * 60)

            finally:
                time.sleep(5)

    time.sleep(5)
