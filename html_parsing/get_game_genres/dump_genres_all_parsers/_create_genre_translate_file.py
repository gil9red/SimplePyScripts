#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import json

from db import Game

json.dump(
    dict.fromkeys(Game.get_all_genres()),
    open('genre_translate.json', 'w', encoding='utf-8'),
    ensure_ascii=False,
    indent=4
)

