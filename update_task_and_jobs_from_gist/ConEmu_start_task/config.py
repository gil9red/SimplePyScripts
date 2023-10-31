#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import winshell
from pathlib import Path


DIR = Path(__file__).resolve().parent
GIST_URL = (DIR / "GIST_URL.txt").read_text("utf-8")

DIR_GIST_FILES = DIR / "gists"
DIR_GIST_FILES.mkdir(parents=True, exist_ok=True)

PATH_CONEMU = Path(r"C:\Program Files\ConEmu\ConEmu64.exe")
if not PATH_CONEMU.exists():
    raise FileNotFoundError(PATH_CONEMU)

FILE_NAME_CONEMU_SETTINGS = DIR / "conemu_settings.xml"

PREFIX_LINK = "ConEmu start task"

DIR_STARTUP = Path(winshell.startup())
