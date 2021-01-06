#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT
import logging
import time
import traceback
import sys
from typing import Optional, Tuple

# pip install pyautogui
import pyautogui

# pip install psutil
import psutil

# pip install schedule
import schedule


pyautogui.FAILSAFE = False


def is_exists_rdp_process() -> bool:
    for process in psutil.process_iter():
        if process.name() == 'mstsc.exe':
            return True

    return False


logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s',
    stream=sys.stdout,
)


def get_pos_rdp_task_icon() -> Optional[Tuple[int, int]]:
    try:
        return pyautogui.locateCenterOnScreen("RDP_task_icon.png", minSearchTime=5)
    except:
        pass


def run():
    logging.info("")
    logging.info("Run")

    if DT.date.today().weekday() in [5, 6]:
        logging.info("Today is a weekend, skip")
        return

    if not is_exists_rdp_process():
        logging.info("RDP is not running!")
        return

    try:
        # Сделаем скриншот, чтобы проверить, что после клика
        # картинка поменяется (ждем пока свернутся окна)
        img = pyautogui.screenshot()
        for _ in range(5):
            # Свернуть все окна
            pyautogui.hotkey('win', 'd')
            time.sleep(2)

            if img != pyautogui.screenshot():
                break

        pos = get_pos_rdp_task_icon()
        logging.info(f'1. get_pos_rdp_task_icon: {pos}')
        if not pos:
            # Нужно сдвинуть курсор туда, где точно не может находиться кнопка задачи RPD,
            # это поможет если курсор уже находится на кнопке задачи RDP
            pyautogui.moveTo(300, 300)

        time.sleep(2)

        pos = get_pos_rdp_task_icon()
        logging.info(f'2. get_pos_rdp_task_icon: {pos}')
        if pos:
            pyautogui.click(*pos)
            logging.info("Click")

    except Exception as e:
        print(traceback.format_exc())


if __name__ == '__main__':
    logging.info("Started...")

    # Каждый день в 07:00
    schedule \
        .every().day.at("07:00") \
        .do(run)

    logging.info('Jobs:')
    for job in schedule.jobs:
        logging.info(f'    {job}')

    logging.info('')

    while True:
        schedule.run_pending()
        time.sleep(1)

