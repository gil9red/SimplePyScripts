#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT

import sys
sys.path.append('../wait')
from wait import wait

from get_assigned_open_issues_per_project import get_and_prints
import db


while True:
    try:
        print(f'Начало в {DT.date.today()}\n')

        assigned_open_issues_per_project = get_and_prints()
        print()

        ok = db.add(assigned_open_issues_per_project)
        if ok is None:
            print("Количество открытых задач в проектах не поменялось. Пропускаю...")

        print('\n' + '-' * 100 + '\n')
        wait(days=1)

    except Exception:
        import traceback
        print('Ошибка:')
        print(traceback.format_exc())

        print('Через 15 минут попробую снова...')
        wait(minutes=15)
