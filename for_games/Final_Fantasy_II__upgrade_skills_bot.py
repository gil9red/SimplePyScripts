#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Using ePSXe + setting in the joystick buttons "X" as "K" and "O" as "L".
"""


import logging
import os
import time
import sys

from logging.handlers import RotatingFileHandler

import keyboard

from press_release_keys__ScanCodes__for_games import write_key, DIK_L, DIK_K, DIK_S


def get_logger(name, file="log.txt", encoding="utf-8", log_stdout=True, log_file=True):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s"
    )

    if log_file:
        fh = RotatingFileHandler(
            file, maxBytes=10000000, backupCount=5, encoding=encoding
        )
        fh.setFormatter(formatter)
        log.addHandler(fh)

    if log_stdout:
        sh = logging.StreamHandler(stream=sys.stdout)
        sh.setFormatter(formatter)
        log.addHandler(sh)

    return log


def change_start():
    DATA["START"] = not DATA["START"]
    if DATA["START"]:
        DATA["COUNTER"] = 0

    log.debug("Change START: %s", DATA["START"])


def set_min_counter():
    DATA["MAX_COUNTER"] = 1
    log.debug("Change MAX_COUNTER: %s", DATA["MAX_COUNTER"])


def set_max_counter():
    DATA["MAX_COUNTER"] = MAX_COUNTER
    log.debug("Change MAX_COUNTER: %s", DATA["MAX_COUNTER"])


def change_cancel_all_last():
    DATA["CANCEL_ALL_LAST"] = not DATA["CANCEL_ALL_LAST"]
    log.debug("Change CANCEL_ALL_LAST: %s", DATA["CANCEL_ALL_LAST"])


RUN_COMBINATION = "Ctrl+Shift+Space"
RUN_SET_MIN_COUNTER = "Ctrl+Shift+1"
RUN_SET_MAX_COUNTER = "Ctrl+Shift+2"
RUN_CHANGE_CANCEL_ALL_LAST = "Ctrl+Shift+3"
QUIT_COMBINATION = "Ctrl+Shift+Q"

MAX_COUNTER = 100

DATA = {
    "START": False,
    "COUNTER": 0,
    "MAX_COUNTER": MAX_COUNTER,
    "CANCEL_ALL_LAST": True,
}

log = get_logger(__file__, log_file=False)

log.debug('Press "%s" for RUN / PAUSE', RUN_COMBINATION)
log.debug('Press "%s" for RUN_SET_MIN_COUNTER', RUN_SET_MIN_COUNTER)
log.debug('Press "%s" for RUN_SET_MAX_COUNTER', RUN_SET_MAX_COUNTER)
log.debug('Press "%s" for RUN_CHANGE_CANCEL_ALL_LAST', RUN_CHANGE_CANCEL_ALL_LAST)
log.debug('Press "%s" for QUIT', QUIT_COMBINATION)
log.debug("DATA: %s", DATA)

keyboard.add_hotkey(RUN_COMBINATION, change_start)
keyboard.add_hotkey(RUN_SET_MIN_COUNTER, set_min_counter)
keyboard.add_hotkey(RUN_SET_MAX_COUNTER, set_max_counter)
keyboard.add_hotkey(RUN_CHANGE_CANCEL_ALL_LAST, change_cancel_all_last)
keyboard.add_hotkey(
    QUIT_COMBINATION, lambda: log.debug("Quit by Escape") or os._exit(0)
)


while True:
    if not DATA["START"]:
        time.sleep(0.01)
        continue

    # Прокачка атаки
    # # Симуляция атаки, кнопка K
    # for _ in range(6):
    #     write_key(DIK_K, pause=0.3)

    number = 3
    if not DATA["CANCEL_ALL_LAST"]:
        number = 4

    # Прокачка магии
    # Симуляция выбора первого заклинания магии
    for _ in range(number):
        write_key(DIK_S, pause=0.3)
        write_key(DIK_K, pause=0.3)
        write_key(DIK_K, pause=0.3)
        write_key(DIK_K, pause=0.3)

    if DATA["CANCEL_ALL_LAST"]:
        # Отмена атаки, кнопка L
        # https://gist.github.com/tracend/912308#file-gistfile1-cpp-L42
        for _ in range(4):
            write_key(DIK_L, pause=0.3)

    # 100 итераций должно хватить, чтобы докачать до 100% уровень оружия
    DATA["COUNTER"] += 1
    if DATA["COUNTER"] >= DATA["MAX_COUNTER"]:
        DATA["START"] = False
        log.debug("Change START: %s", DATA["START"])
