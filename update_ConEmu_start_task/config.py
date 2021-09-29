#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import re
from pathlib import Path


DIR = Path(__file__).resolve().parent
GIST_URL = (DIR / 'GIST_URL.txt').read_text('utf-8')

DIR_GIST_FILES = DIR / 'gists'
DIR_GIST_FILES.mkdir(parents=True, exist_ok=True)

DIR_LNKS = DIR / 'lnks'
DIR_LNKS.mkdir(parents=True, exist_ok=True)

PATH_CONEMU = Path(r'C:\Program Files (x86)\ConEmu\ConEmu.exe')
if not PATH_CONEMU.exists():
    raise FileNotFoundError(PATH_CONEMU)

FILE_NAME_CONEMU_SETTINGS = DIR / 'conemu_settings.xml'

PATTERN_NAME_TASK = 'My python {}'
RE_PATTERN_CONEMU_TASK = re.compile(r'^{My python \d+}$', flags=re.IGNORECASE)

RE_PATTERN_FILE_TASK = re.compile(r'^group(\d+)$')
