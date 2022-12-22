#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT
import sys
import traceback

from pathlib import Path


DIR = Path(__file__).resolve().parent

# Import https://github.com/gil9red/SimplePyScripts/blob/8fa9b9c23d10b5ee7ff0161da997b463f7a861bf/wait/wait.py
sys.path.append(str(DIR.parent.parent / 'wait'))
sys.path.append(str(DIR.parent))
from wait import wait
from get_profile_rating import get_profile_rating


from db import ProfileRating, db_create_backup


URL = 'https://pikabu.ru/@user4942077'


while True:
    print(f'Started at {DT.datetime.now():%d/%m/%Y %H:%M:%S}\n')

    db_create_backup()

    try:
        value = get_profile_rating(URL)
        print(f'URL: {URL}\n     {value}\n')

        ProfileRating.append(URL, value)

        wait(weeks=1)

    except Exception as e:
        # Выводим ошибку в консоль
        tb = traceback.format_exc()
        print(tb)

        print('Wait 15 minutes')
        wait(minutes=15)

    print()
