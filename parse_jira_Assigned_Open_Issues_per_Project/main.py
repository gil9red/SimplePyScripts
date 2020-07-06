#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT

import sys
sys.path.append('../wait')
from wait import wait

from get_assigned_open_issues_per_project import get_and_prints
import db


def run():
    while True:
        try:
            print(f'Начало в {DT.date.today()}\n')

            assigned_open_issues_per_project = get_and_prints()
            print()

            ok = db.add(assigned_open_issues_per_project)
            if ok is None:
                print("Количество открытых задач в проектах не поменялось. Пропускаю...")
            elif ok:
                print("Добавляю запись")
            else:
                print("Сегодня запись уже была добавлена. Пропускаю...")

            print('\n' + '-' * 100 + '\n')
            break

        except Exception:
            import traceback
            print('Ошибка:')
            print(traceback.format_exc())

            print('Через 15 минут попробую снова...')
            wait(minutes=15)


if __name__ == '__main__':
    # pip install schedule
    import schedule
    import time

    schedule.every().day.at("20:00").do(run)

    while True:
        schedule.run_pending()
        time.sleep(1)
