#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'ipetrash'


import threading
import os
import cv2
import numpy as np
import pyautogui
from timeit import default_timer as timer
from datetime import datetime
import time


# TODO: можно вынести в common.py: get_logger, get_current_datetime_str, find_contours, find_rect_contours


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


log = get_logger('Bot Buff Knight Advanced')


def get_current_datetime_str():
    return datetime.now().strftime('%d%m%y %H%M%S.%f')


def find_contours(image_source_hsv, hsv_min, hsv_max):
    thresholded_image = image_source_hsv

    # Отфильтровываем только то, что нужно, по диапазону цветов
    thresholded_image = cv2.inRange(
        thresholded_image,
        np.array(hsv_min, np.uint8),
        np.array(hsv_max, np.uint8)
    )

    # Убираем шум
    thresholded_image = cv2.erode(
        thresholded_image,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    )
    thresholded_image = cv2.dilate(
        thresholded_image,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    )

    # Замыкаем оставшиеся крупные объекты
    thresholded_image = cv2.dilate(
        thresholded_image,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    )
    thresholded_image = cv2.erode(
        thresholded_image,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    )

    # Находим контуры
    _, contours, hierarchy = cv2.findContours(
        thresholded_image,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    return contours


def find_rect_contours(image_source_hsv, hsv_min, hsv_max):
    return [cv2.boundingRect(c) for c in find_contours(image_source_hsv, hsv_min, hsv_max)]


# def draw_rects(img, contours_rects, color=(0, 255, 0)):
#     for x, y, w, h in contours_rects:
#         cv2.rectangle(img, (x, y), (x + w, y + h), color, thickness=5)
#         # cv2.rectangle(img, (x, y), (x + w, y + h), color, thickness=-1)
#
#         for i in range(h // 10):
#             cv2.line(img, (x, y + i * 10 + 5), (x + w, y + i * 10 + 5), color, thickness=2)
#
#         cv2.line(img, (0, y), (img.shape[1], y), color, thickness=1)


def filter_button(rect):
    x, y, w, h = rect

    # TODO: эффективнее для разных разрешений сравнивать процентно, а не пиксельно

    rule_1 = w > 30 and h > 30
    rule_2 = w > h

    # if not rule_1:
    #     print('filter_button. Fail rule_1')
    #
    # if not rule_2:
    #     print('filter_button. Fail rule_2')

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

    # if not rule_1:
    #     print('filter_fairy. Fail rule_1')
    #
    # if not rule_2:
    #     print('filter_fairy. Fail rule_2')
    #
    # if not rule_3:
    #     print('filter_fairy. Fail rule_3')

    return rule_1 and rule_2 and rule_3


def filter_fairy_and_button(rect_fairy, rect_button):
    x, y = rect_fairy[:2]
    x2, y2, _, h2 = rect_button

    # TODO: эффективнее для разных разрешений сравнивать процентно, а не пиксельно
    return abs(x2 - x) <= 50 and abs(y2 + h2 - y) <= 50


DIR = 'saved_screenshots'


def save_screenshot(prefix, img_hsv):
    file_name = DIR + '/{}__{}.png'.format(prefix, get_current_datetime_str())
    log.debug(file_name)
    cv2.imwrite(file_name, cv2.cvtColor(np.array(img_hsv), cv2.COLOR_HSV2BGR))


BLUE_HSV_MIN = 105, 175, 182
BLUE_HSV_MAX = 121, 255, 255

ORANGE_HSV_MIN = 7, 200, 200
ORANGE_HSV_MAX = 20, 255, 255

FAIRY_HSV_MIN = 73, 101, 101
FAIRY_HSV_MAX = 95, 143, 255


RUN_COMBINATION = 'Ctrl+Shift+R'
QUIT_COMBINATION = 'Ctrl+Shift+Q'
AUTO_ATTACK_COMBINATION = 'Space'

BOT_DATA = {
    'START': False,
    'AUTO_ATTACK': False,
}


def change_start():
    BOT_DATA['START'] = not BOT_DATA['START']
    print('START:', BOT_DATA['START'])


def change_auto_attack():
    BOT_DATA['AUTO_ATTACK'] = not BOT_DATA['AUTO_ATTACK']
    print('AUTO_ATTACK:', BOT_DATA['AUTO_ATTACK'])


print('Press "{}" for RUN / PAUSE'.format(RUN_COMBINATION))
print('Press "{}" for QUIT'.format(QUIT_COMBINATION))
print('Press "{}" for AUTO_ATTACK'.format(AUTO_ATTACK_COMBINATION))


if not os.path.exists(DIR):
    os.mkdir(DIR)

# TODO: возможность автоматического использования хилок и восстановления маны

import keyboard
keyboard.add_hotkey(QUIT_COMBINATION, lambda: print('Quit by Escape') or os._exit(0))
keyboard.add_hotkey(AUTO_ATTACK_COMBINATION, change_auto_attack)
keyboard.add_hotkey(RUN_COMBINATION, change_start)


def process_auto_attack():
    # i = 1

    while True:
        if not BOT_DATA['START']:
            time.sleep(0.01)
            continue

        # print(i, 'AUTO_ATTACK:', BOT_DATA['AUTO_ATTACK'])

        # Симуляция атаки
        if BOT_DATA['AUTO_ATTACK']:
            pyautogui.typewrite('C')

        time.sleep(0.01)
        # i += 1

# Запуск потока для автоатаки
thread_auto_attack = threading.Thread(target=process_auto_attack)
thread_auto_attack.start()


while True:
    if not BOT_DATA['START']:
        time.sleep(0.01)
        continue

    t = timer()

    img_screenshot = pyautogui.screenshot()
    log.debug('img_screenshot: %s', img_screenshot)

    img = cv2.cvtColor(np.array(img_screenshot), cv2.COLOR_RGB2HSV)

    try:
        rects_blue = find_rect_contours(img, BLUE_HSV_MIN, BLUE_HSV_MAX)
        rects_orange = find_rect_contours(img, ORANGE_HSV_MIN, ORANGE_HSV_MAX)
        rects_fairy = find_rect_contours(img, FAIRY_HSV_MIN, FAIRY_HSV_MAX)

        # Фильтрование оставшихся объектов
        rects_blue = list(filter(filter_button, rects_blue))
        rects_orange = list(filter(filter_button, rects_orange))
        rects_fairy = list(filter(filter_fairy, rects_fairy))

        if rects_blue or rects_orange:
            new_rects_fairy = []

            # Фея и кнопки находятся рядом, поэтому имеет смысл убрать те "феи", что не имеют рядом синих или оранжевых
            for rect_fairy in rects_fairy:
                x, y = rect_fairy[:2]

                found_blue = bool(list(filter(lambda rect: filter_fairy_and_button(rect_fairy, rect), rects_blue)))
                found_orange = bool(list(filter(lambda rect: filter_fairy_and_button(rect_fairy, rect), rects_orange)))

                if found_blue or found_orange:
                    new_rects_fairy.append(rect_fairy)

            rects_fairy = new_rects_fairy

        if not rects_fairy:
            continue

        if len(rects_fairy) > 1:
            save_screenshot('many_fairy', img)
            continue

        # Фильтр кнопок. Нужно оставить только те кнопки, что рядом с феей
        rect_fairy = rects_fairy[0]
        rects_blue = list(filter(lambda rect: filter_fairy_and_button(rect_fairy, rect), rects_blue))
        rects_orange = list(filter(lambda rect: filter_fairy_and_button(rect_fairy, rect), rects_orange))

        # Если одновременно обе кнопки
        if rects_blue and rects_orange:
            save_screenshot('many_buttons', img)
            continue

        if not rects_blue and not rects_orange:
            continue

        # Найдена синяя кнопка
        if rects_blue:
            log.debug('FOUND BLUE')
            save_screenshot('found_blue', img)

            pyautogui.typewrite('D')

        # Найдена оранжевая кнопка
        if rects_orange:
            log.debug('FOUND ORANGE')
            save_screenshot('found_orange', img)

            pyautogui.typewrite('A')

        # print('rects_blue({}): {}'.format(len(rects_blue), rects_blue))
        # print('rects_orange({}): {}'.format(len(rects_orange), rects_orange))
        # print('rects_fairy({}): {}'.format(len(rects_fairy), rects_fairy))
        #
        # draw_rects(img, rects_blue, (255, 0, 0))
        # draw_rects(img, rects_orange, (0, 0, 255))
        # draw_rects(img, rects_fairy, (255, 255, 255))
        #
        # cv2.putText(img, 'blue ' + str(rects_blue), (10, 500 + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        # cv2.putText(img, 'orange ' + str(rects_orange), (10, 500 + 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        # cv2.putText(img, 'fairy ' + str(rects_fairy), (10, 500 + 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    finally:
        log.debug('Elapsed: {} secs'.format(timer() - t))

        time.sleep(0.01)

        # cv2.imshow('img_with_rect ' + file_name, img_with_rect)
