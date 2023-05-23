#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path
from common import download


DIR = Path(__file__).resolve().parent

DIR_VIDEO = DIR / Path(__file__).stem
DIR_VIDEO.mkdir(parents=True, exist_ok=True)

URL = "https://stopgame.ru/gamemovie/genre/guild"

download(DIR_VIDEO, URL)
