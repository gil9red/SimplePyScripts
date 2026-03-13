#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path
import requests


DIR: Path = Path(__file__).resolve().parent

DIR_DUMPS: Path = DIR / "dumps"
DIR_DUMPS.mkdir(parents=True, exist_ok=True)

session = requests.Session()
