#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys
from pathlib import Path


DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))
sys.path.append(str(ROOT_DIR.parent))
from html_parsing.ru_wiktionary_org__wiki__Список_частотных_слов_русского_языка_2013 import get_words
from pymorphy2__examples.normal_form import get_normal_form

import db


for word in get_words():
    word = get_normal_form(word)
    db.Word2Emoji.add(word)
