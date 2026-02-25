#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import threading
import os
import time

from timeit import default_timer as timer

# pip install opencv-python
import cv2
import numpy as np
import pyautogui
import keyboard

from common import get_logger, get_current_datetime_str, find_rect_contours


def filter_button(rect):
    x, y, w, h = rect

    # TODO: эффективнее для разных разрешений сравнивать процентно, а не пиксельно

    rule_1 = w > 30 and h > 30
    rule_2 = w > h

    # У кнопок ширина больше высоты
    return rule_1 and rule_2


def filter_fairy(rect):
    x, y, w, h = rect

    # TODO: эффективнее для разных разрешений сравнивать процентно, а не пиксельно

    # У феи ширина и высота больше определенной цифры
    rule_1 = w > 20 and h > 20

    # У феи высота больше ширины
    rule_2 = h > w

    # Фея приблизительно по центру экрана летает
    rule_3 = y > 300 and y < 900

    return rule_1 and rule_2 and rule_3


def filter_fairy_and_button(rect_fairy, rect_button):
    x, y = rect_fairy[:2]
    x2, y2, _, h2 = rect_button

    # TODO: эффективнее для разных разрешений сравнивать процентно, а не пиксельно
    return abs(x2 - x) <= 50 and abs(y2 + h2 - y) <= 50


DIR = "saved_screenshots"
if not os.path.exists(DIR):
    os.mkdir(DIR)


def save_screenshot(prefix, img_hsv) -> None:
    file_name = f"{DIR}/{prefix}__{get_current_datetime_str()}.png"
    log.debug(file_name)
    cv2.imwrite(file_name, cv2.cvtColor(np.array(img_hsv), cv2.COLOR_HSV2BGR))


log = get_logger("Bot Buff Knight Advanced")


BLUE_HSV_MIN = 105, 175, 182
BLUE_HSV_MAX = 121, 255, 255

ORANGE_HSV_MIN = 7, 200, 200
ORANGE_HSV_MAX = 20, 255, 255

FAIRY_HSV_MIN = 73, 101, 101
FAIRY_HSV_MAX = 95, 143, 255


RUN_COMBINATION = "Ctrl+Shift+R"
QUIT_COMBINATION = "Ctrl+Shift+Q"
AUTO_ATTACK_COMBINATION = "Space"

BOT_DATA = {
    "START": False,
    "AUTO_ATTACK": False,
}


def change_start() -> None:
    BOT_DATA["START"] = not BOT_DATA["START"]
    log.debug("START: %s", BOT_DATA["START"])


def change_auto_attack() -> None:
    BOT_DATA["AUTO_ATTACK"] = not BOT_DATA["AUTO_ATTACK"]
    log.debug("AUTO_ATTACK: %s", BOT_DATA["AUTO_ATTACK"])


log.debug('Press "%s" for RUN / PAUSE', RUN_COMBINATION)
log.debug('Press "%s" for QUIT', QUIT_COMBINATION)
log.debug('Press "%s" for AUTO_ATTACK', AUTO_ATTACK_COMBINATION)


def process_auto_attack() -> None:
    while True:
        if not BOT_DATA["START"]:
            time.sleep(0.01)
            continue

        # Симуляция атаки
        if BOT_DATA["AUTO_ATTACK"]:
            pyautogui.typewrite("C")

        time.sleep(0.01)


def process_find_fairy(img_hsv) -> None:
    rects_blue = find_rect_contours(img_hsv, BLUE_HSV_MIN, BLUE_HSV_MAX)
    rects_orange = find_rect_contours(img_hsv, ORANGE_HSV_MIN, ORANGE_HSV_MAX)
    rects_fairy = find_rect_contours(img_hsv, FAIRY_HSV_MIN, FAIRY_HSV_MAX)

    # Фильтрование оставшихся объектов
    rects_blue = list(filter(filter_button, rects_blue))
    rects_orange = list(filter(filter_button, rects_orange))
    rects_fairy = list(filter(filter_fairy, rects_fairy))

    # Фильтр объектов, похожих на фею
    if rects_blue or rects_orange:
        new_rects_fairy = []

        # Фея и кнопки находятся рядом, поэтому имеет смысл убрать те "феи", что не имеют рядом синих или оранжевых
        for rect_fairy in rects_fairy:
            found_blue = bool(
                list(
                    filter(
                        lambda rect: filter_fairy_and_button(rect_fairy, rect),
                        rects_blue,
                    )
                )
            )
            found_orange = bool(
                list(
                    filter(
                        lambda rect: filter_fairy_and_button(rect_fairy, rect),
                        rects_orange,
                    )
                )
            )

            # Если возле феи что-то нашлось
            if found_blue or found_orange:
                new_rects_fairy.append(rect_fairy)

        rects_fairy = new_rects_fairy

    if not rects_fairy:
        return

    if len(rects_fairy) > 1:
        save_screenshot("many_fairy", img_hsv)
        return

    # Фильтр кнопок. Нужно оставить только те кнопки, что рядом с феей
    rect_fairy = rects_fairy[0]
    rects_blue = list(
        filter(lambda rect: filter_fairy_and_button(rect_fairy, rect), rects_blue)
    )
    rects_orange = list(
        filter(lambda rect: filter_fairy_and_button(rect_fairy, rect), rects_orange)
    )

    # Если одновременно обе кнопки
    if rects_blue and rects_orange:
        save_screenshot("many_buttons", img_hsv)
        return

    if not rects_blue and not rects_orange:
        return

    # Найдена синяя кнопка
    if rects_blue:
        log.debug("FOUND BLUE")
        save_screenshot("found_blue", img)

        pyautogui.typewrite("D")

    # Найдена оранжевая кнопка
    if rects_orange:
        log.debug("FOUND ORANGE")
        save_screenshot("found_orange", img)

        pyautogui.typewrite("A")


if __name__ == "__main__":
    keyboard.add_hotkey(
        QUIT_COMBINATION, lambda: log.debug("Quit by Escape") or os._exit(0)
    )
    keyboard.add_hotkey(AUTO_ATTACK_COMBINATION, change_auto_attack)
    keyboard.add_hotkey(RUN_COMBINATION, change_start)

    # Запуск потока для автоатаки
    thread_auto_attack = threading.Thread(target=process_auto_attack)
    thread_auto_attack.start()

    while True:
        if not BOT_DATA["START"]:
            time.sleep(0.01)
            continue

        t = timer()

        try:
            img_screenshot = pyautogui.screenshot()
            log.debug("img_screenshot: %s", img_screenshot)

            img = cv2.cvtColor(np.array(img_screenshot), cv2.COLOR_RGB2HSV)

            # Поиск феи
            process_find_fairy(img)

            # TODO: возможность автоматического использования хилок и восстановления маны

        finally:
            log.debug(f"Elapsed: {timer() - t} secs")

            time.sleep(0.01)
