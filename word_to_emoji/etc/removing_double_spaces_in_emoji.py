#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))
import db


for x in db.Word2Emoji.select().where(db.Word2Emoji.emoji.contains("  ")):
    emoji = db.preprocess_emoji(x.emoji)
    if emoji != x.emoji:
        x.emoji = emoji
        x.save()
