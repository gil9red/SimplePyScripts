#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
import sys
import time

# OpenCv -- for performance
# pip install opencv-python
#
# pip install pyautogui
import pyautogui


def go():
    OPEN_SMILE_MENU = "elements/open_smile_menu.png"
    GROUP_SMILE = "elements/group_smile.png"
    CLICK_SMILE = "elements/click_smile.png"
    SEND = "elements/send.png"

    def get_logger():
        log = logging.getLogger("telegram_smile_clicker")
        log.setLevel(logging.DEBUG)

        sh = logging.StreamHandler(stream=sys.stdout)
        sh.setFormatter(logging.Formatter("[%(asctime)s] %(message)s"))
        log.addHandler(sh)

        return log

    log = get_logger()
    log_it = lambda pos, filename: log.debug("{} [{}]".format(pos, filename))

    # Ищем меню с смайлами
    pos = pyautogui.locateCenterOnScreen(OPEN_SMILE_MENU)
    log_it(pos, OPEN_SMILE_MENU)
    if not pos:
        return

    # Показываем меню с смайлами
    pyautogui.moveTo(pos)

    # Ожидаем
    time.sleep(1)

    # Ищем наш смайл в меню
    pos = pyautogui.locateCenterOnScreen(CLICK_SMILE)
    log_it(pos, CLICK_SMILE)
    if pos:
        # Кликаем на смайл
        pyautogui.click(pos)

    else:
        # Ищем группу, в которой наш смайл
        pos = pyautogui.locateCenterOnScreen(GROUP_SMILE)
        log_it(pos, GROUP_SMILE)
        if not pos:
            return

        # Кликаем на группу, в которой наш смайл
        pyautogui.click(pos)

        # Ищем наш смайл в меню
        pos = pyautogui.locateCenterOnScreen(CLICK_SMILE)
        log_it(pos, CLICK_SMILE)
        if not pos:
            return

        # Кликаем на смайл
        pyautogui.click(pos)

    # Ищем кнопку SEND
    pos = pyautogui.locateCenterOnScreen(SEND)
    log_it(pos, SEND)
    if not pos:
        return

    # Кликаем на кнопку SEND
    pyautogui.click(pos)


if __name__ == "__main__":
    # import profile
    # profile.run('go()')

    go()
