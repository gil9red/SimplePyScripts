# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
#
# __author__ = 'ipetrash'
#
#
# def init_db():
#     from common import create_connect
#
#     # Создание базы и таблицы
#     connect = create_connect()
#     try:
#         connect.execute('''
#             CREATE TABLE IF NOT EXISTS Game (
#                 id INTEGER PRIMARY KEY,
#
#                 name TEXT NOT NULL,
#                 price TEXT DEFAULT NULL,
#                 modify_date TIMESTAMP DEFAULT NULL,
#                 kind TEXT NOT NULL,
#                 check_steam BOOLEAN NOT NULL DEFAULT 0
#             );
#         ''')
#
#         connect.commit()
#
#         # NOTE: когда нужно в таблице подправить схему:
#         # cursor.executescript('''
#         # DROP TABLE Game2;
#         #
#         # CREATE TABLE IF NOT EXISTS Game2 (
#         #     id INTEGER PRIMARY KEY,
#         #
#         #     name TEXT NOT NULL,
#         #     price TEXT DEFAULT NULL,
#         #     modify_date TIMESTAMP DEFAULT NULL,
#         #     kind TEXT NOT NULL,
#         #     check_steam BOOLEAN NOT NULL DEFAULT 0
#         # );
#         #
#         # INSERT INTO Game2 SELECT * FROM Game;
#         #
#         # DROP TABLE Game;
#         # ALTER TABLE Game2 RENAME TO Game;
#         #
#         # ''')
#         #
#         # connect.commit()
#
#     finally:
#         connect.close()
#
#
# def wait(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
#     from datetime import timedelta
#     today = datetime.today()
#     timeout_date = today + timedelta(
#         days=days, seconds=seconds, microseconds=microseconds,
#         milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks
#     )
#
#     while today <= timeout_date:
#         def str_timedelta(td):
#             mm, ss = divmod(td.seconds, 60)
#             hh, mm = divmod(mm, 60)
#             return "%d:%02d:%02d" % (hh, mm, ss)
#
#         left = timeout_date - today
#         left = str_timedelta(left)
#
#         print('\r' * 100, end='')
#         print('До следующего запуска осталось {}'.format(left), end='')
#
#         import sys
#         sys.stdout.flush()
#
#         # Delay 1 seconds
#         import time
#         time.sleep(1)
#
#         today = datetime.today()
#
#     print('\r' * 100, end='')
#     print('\n')
#
#
# while True:
#     try:
#         # Перед выполнением, запоминаем дату и время, чтобы иметь потом представление когда
#         # в последний раз выполнялось заполнение списка
#         from datetime import datetime
#         today = datetime.today()
#         print(today)
#
#
#
#         # Every 5 minutes
#         wait(minutes=5)
#
#     except Exception:
#         import traceback
#         print('Ошибка:')
#         print(traceback.format_exc())
#
#         print('Через 5 минут попробую снова...')
#
#         # Wait 5 minutes before next attempt
#         import time
#         time.sleep(5 * 60)
