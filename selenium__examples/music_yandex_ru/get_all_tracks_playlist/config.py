#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os.path
from pathlib import Path

# pip install selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


profile_directory = os.path.expandvars(
    r"%AppData%\Mozilla\Firefox\Profiles\p75l82q1.for_mail__selenium"
)
profile = webdriver.FirefoxProfile(profile_directory)

options_headless = Options()
options_headless.add_argument("--headless")

url = "https://music.yandex.ru/users/ilyapetrash/playlists/3"

DIR_DUMP = Path(__file__).resolve().parent / "dumps"
DIR_DUMP.mkdir(exist_ok=True)
