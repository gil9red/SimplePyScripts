#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import time
import traceback

# pip install translate
from translate import Translator

import db
from html_parsing.emojipedia_org__search import get_emoji


translator = Translator(from_lang="ru", to_lang='en')


for word_ru in db.Word2Emoji.get_unprocessed_words():
    try:
        # На emojipedia поиск нужен на английском
        word = translator.translate(word_ru)
        emoji = get_emoji(word)
        if not emoji:
            continue

        print(f'Add {word_ru!r} ({word!r}) -> {emoji!r}')
        db.Word2Emoji.add(word_ru, emoji)

    except:
        print(traceback.format_exc())

    finally:
        time.sleep(5)
