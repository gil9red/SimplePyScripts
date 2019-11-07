#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT

# Import https://github.com/gil9red/SimplePyScripts/blob/8fa9b9c23d10b5ee7ff0161da997b463f7a861bf/wait/wait.py
import sys
sys.path.append('../wait')
sys.path.append('../html_parsing')

from wait import wait
from get_stackoverflow_people_reached import get_stackoverflow_people_reached

from db import PeopleReached, db_create_backup


URL = 'https://ru.stackoverflow.com/users/201445/gil9red'


while True:
    print(f'Started at {DT.datetime.now():%d/%m/%Y %H:%M:%S}\n')

    db_create_backup()

    try:
        value = get_stackoverflow_people_reached(URL)
        print(f'URL: {URL}\n     {value}\n')

        PeopleReached.append(URL, value)

        wait(weeks=1)

    except Exception as e:
        # Выводим ошибку в консоль
        import traceback
        tb = traceback.format_exc()
        print(tb)

        print('Wait 15 minutes')
        wait(minutes=15)

    print()
