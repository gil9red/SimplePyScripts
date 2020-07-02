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
        print(f'Started as {DT.date.today()}\n')

        assigned_open_issues_per_project = get_and_prints()
        db.add(assigned_open_issues_per_project)

        print('\n' + '-' * 100 + '\n')
        wait(weeks=1)

    except Exception:
        import traceback
        print('Ошибка:')
        print(traceback.format_exc())

        print('Через 15 минут попробую снова...')
        wait(minutes=15)
