#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Using ePSXe + setting in the joystick buttons "X" as "K" and "O" as "L".
"""


import os
import time

import keyboard

from press_release_keys__ScanCodes__for_games import write_key, DIK_L, DIK_K


def get_logger(name, file='log.txt', encoding='utf-8', log_stdout=True, log_file=True):
    import logging
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s')

    if log_file:
        from logging.handlers import RotatingFileHandler
        fh = RotatingFileHandler(file, maxBytes=10000000, backupCount=5, encoding=encoding)
        fh.setFormatter(formatter)
        log.addHandler(fh)

    if log_stdout:
        import sys
        sh = logging.StreamHandler(stream=sys.stdout)
        sh.setFormatter(formatter)
        log.addHandler(sh)

    return log


RUN_COMBINATION = 'Ctrl+Shift+R'
QUIT_COMBINATION = 'Ctrl+Shift+Q'

DATA = {
    'START': False,
    'COUNTER': 0,
}

log = get_logger(__file__, log_file=False)


def change_start():
    DATA['START'] = not DATA['START']
    if DATA['START']:
        DATA['COUNTER'] = 0

    log.debug('START: %s', DATA['START'])


log.debug('Press "%s" for RUN / PAUSE', RUN_COMBINATION)
log.debug('Press "%s" for QUIT', QUIT_COMBINATION)


keyboard.add_hotkey(QUIT_COMBINATION, lambda: log.debug('Quit by Escape') or os._exit(0))
keyboard.add_hotkey(RUN_COMBINATION, change_start)


while True:
    if not DATA['START']:
        time.sleep(0.01)
        continue

    # Симуляция атаки, кнопка K
    for _ in range(6):
        write_key(DIK_K, pause=0.3)

    # Отмена атаки, кнопка L
    # https://gist.github.com/tracend/912308#file-gistfile1-cpp-L42
    for _ in range(6):
        write_key(DIK_L, pause=0.3)

    # 100 итераций должно хватить, чтобы докачать до 100% уровень оружия
    DATA['COUNTER'] += 1
    if DATA['COUNTER'] == 100:
        DATA['START'] = False
