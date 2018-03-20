#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'ipetrash'


import cv2
import numpy as np
import pyautogui
from timeit import default_timer as timer
from datetime import datetime


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


def draw_rects(img, contours_rects, color=(0, 255, 0)):
    for x, y, w, h in contours_rects:
        cv2.rectangle(img, (x, y), (x + w, y + h), color, thickness=5)
        # cv2.rectangle(img, (x, y), (x + w, y + h), color, thickness=-1)

        for i in range(h // 10):
            cv2.line(img, (x, y + i * 10 + 5), (x + w, y + i * 10 + 5), color, thickness=2)

        cv2.line(img, (0, y), (img.shape[1], y), color, thickness=1)


def filter_button(rect):
    x, y, w, h = rect

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
    return abs(x2 - x) <= 50 and abs(y2 + h2 - y) <= 50


# BLUE:   105, 175, 182 / 121, 255, 255
# ORANGE: 7  , 200, 200 / 20 , 255, 255
# FAIRY:  73 , 101, 101 / 95 , 143, 255

BLUE_HSV_MIN = 105, 175, 182
BLUE_HSV_MAX = 121, 255, 255

ORANGE_HSV_MIN = 7, 200, 200
ORANGE_HSV_MAX = 20, 255, 255

FAIRY_HSV_MIN = 73, 101, 101
FAIRY_HSV_MAX = 95, 143, 255

# img_screenshot = pyautogui.screenshot()
# img = cv2.cvtColor(np.array(img_screenshot), cv2.COLOR_RGB2BGR)

import glob

for file_name in glob.glob('screenshots__Buff Knight Advanced/*.png'):
# for file_name in glob.glob('sc/*.png'):
    # if '190930' not in file_name and '190615' not in file_name:continue
    print(file_name)

    # file_name = 'screenshots__Buff Knight Advanced/screenshot_110318 190401.png'
    # file_name = 'screenshots__Buff Knight Advanced/screenshot_110318 190513.png'
    img = cv2.imread(file_name)


    # img = cv2.cvtColor(np.array(img_screenshot), cv2.COLOR_RGB2HSV)
    # img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # # Resize
    # img = cv2.resize(img, None, fx=0.7, fy=0.7, interpolation=cv2.INTER_CUBIC)

    img_screenshot = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image_source_hsv = cv2.cvtColor(np.array(img_screenshot), cv2.COLOR_RGB2HSV)
    # cv2.imshow('img', img)
    print(img.shape[:2])

    img_with_rect = img.copy()

    t = timer()

    try:
        rects_blue = find_rect_contours(image_source_hsv, BLUE_HSV_MIN, BLUE_HSV_MAX)
        rects_orange = find_rect_contours(image_source_hsv, ORANGE_HSV_MIN, ORANGE_HSV_MAX)
        rects_fairy = find_rect_contours(image_source_hsv, FAIRY_HSV_MIN, FAIRY_HSV_MAX)

        # print('rects_fairy:', rects_fairy)

        # Фильтрование оставшихся объектов
        rects_blue = list(filter(filter_button, rects_blue))
        rects_orange = list(filter(filter_button, rects_orange))
        rects_fairy = list(filter(filter_fairy, rects_fairy))

        # print('rects_fairy1:', rects_fairy)

        if rects_blue or rects_orange:
            new_rects_fairy = []

            # Фея и кнопки находятся рядом, поэтому имеет смысл убрать те "феи", что не имеют рядом синих или оранжевых
            for rect_fairy in rects_fairy:
                x, y = rect_fairy[:2]

                found = False

                found_blue = bool(list(filter(lambda rect: filter_fairy_and_button(rect_fairy, rect), rects_blue)))
                found_orange = bool(list(filter(lambda rect: filter_fairy_and_button(rect_fairy, rect), rects_orange)))
                # print(x, y, found_blue or found_orange)

                if found_blue or found_orange:
                    new_rects_fairy.append(rect_fairy)

            rects_fairy = new_rects_fairy

        print('rects_fairy2:', rects_fairy)

        if not rects_fairy:
            continue

        if len(rects_fairy) > 1:
            file_name = 'many_fairy__{}.png'.format(datetime.now().strftime('%d%m%y %H%M%S.%f'))
            print(file_name)
            cv2.imwrite(file_name, img_with_rect)
            continue

        # Фильтр кнопок. Нужно оставить только те кнопки, что рядом с феей
        rect_fairy = rects_fairy[0]
        rects_blue = list(filter(lambda rect: filter_fairy_and_button(rect_fairy, rect), rects_blue))
        rects_orange = list(filter(lambda rect: filter_fairy_and_button(rect_fairy, rect), rects_orange))

        # Если одновременно обе кнопки
        if rects_blue and rects_orange:
            file_name = 'many_buttons__{}.png'.format(datetime.now().strftime('%d%m%y %H%M%S.%f'))
            print(file_name)
            cv2.imwrite(file_name, img_with_rect)
            continue

        if not rects_blue and not rects_orange:
            continue

        print('rects_blue({}): {}'.format(len(rects_blue), rects_blue))
        print('rects_orange({}): {}'.format(len(rects_orange), rects_orange))
        print('rects_fairy({}): {}'.format(len(rects_fairy), rects_fairy))

        draw_rects(img_with_rect, rects_blue, (255, 0, 0))
        draw_rects(img_with_rect, rects_orange, (0, 0, 255))
        draw_rects(img_with_rect, rects_fairy, (255, 255, 255))

        cv2.putText(img_with_rect, 'blue ' + str(rects_blue), (10, 500 + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(img_with_rect, 'orange ' + str(rects_orange), (10, 500 + 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(img_with_rect, 'fairy ' + str(rects_fairy), (10, 500 + 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    finally:
        print('Elapsed: {} secs'.format(timer() - t))
        print()

        cv2.imshow('img_with_rect ' + file_name, img_with_rect)

        # new_file_name = file_name.replace('screenshots__Buff Knight Advanced', 'screenshots__Buff Knight Advanced__filtered')
        # cv2.imwrite(new_file_name, img_with_rect)
        # cv2.imwrite('img_with_rect.png', img_with_rect)

cv2.waitKey()
