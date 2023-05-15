#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = "ipetrash"


import glob
from timeit import default_timer as timer

import cv2
import numpy as np

from main import (
    find_rect_contours,
    filter_button,
    filter_fairy,
    filter_fairy_and_button,
)
from common import get_current_datetime_str


def draw_rects(img, contours_rects, color=(0, 255, 0)):
    for x, y, w, h in contours_rects:
        cv2.rectangle(img, (x, y), (x + w, y + h), color, thickness=5)
        # cv2.rectangle(img, (x, y), (x + w, y + h), color, thickness=-1)

        for i in range(h // 10):
            cv2.line(
                img, (x, y + i * 10 + 5), (x + w, y + i * 10 + 5), color, thickness=2
            )

        cv2.line(img, (0, y), (img.shape[1], y), color, thickness=1)


BLUE_HSV_MIN = 105, 175, 182
BLUE_HSV_MAX = 121, 255, 255

ORANGE_HSV_MIN = 7, 200, 200
ORANGE_HSV_MAX = 20, 255, 255

FAIRY_HSV_MIN = 73, 101, 101
FAIRY_HSV_MAX = 95, 143, 255


for file_name in glob.glob("screenshots__Buff Knight Advanced/*.png"):
    print(file_name)

    img = cv2.imread(file_name)

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
        rects_orange = find_rect_contours(
            image_source_hsv, ORANGE_HSV_MIN, ORANGE_HSV_MAX
        )
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
                # print(x, y, found_blue or found_orange)

                if found_blue or found_orange:
                    new_rects_fairy.append(rect_fairy)

            rects_fairy = new_rects_fairy

        print("rects_fairy2:", rects_fairy)

        if not rects_fairy:
            continue

        if len(rects_fairy) > 1:
            file_name = f"many_fairy__{get_current_datetime_str()}.png"
            print(file_name)
            cv2.imwrite(file_name, img_with_rect)
            continue

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
            file_name = f"many_buttons__{get_current_datetime_str()}.png"
            print(file_name)
            cv2.imwrite(file_name, img_with_rect)
            continue

        if not rects_blue and not rects_orange:
            continue

        print(f"rects_blue({len(rects_blue)}): {rects_blue}")
        print(f"rects_orange({len(rects_orange)}): {rects_orange}")
        print(f"rects_fairy({len(rects_fairy)}): {rects_fairy}")

        draw_rects(img_with_rect, rects_blue, (255, 0, 0))
        draw_rects(img_with_rect, rects_orange, (0, 0, 255))
        draw_rects(img_with_rect, rects_fairy, (255, 255, 255))

        cv2.putText(
            img_with_rect,
            f"blue {rects_blue}",
            (10, 500 + 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )
        cv2.putText(
            img_with_rect,
            f"orange {rects_orange}",
            (10, 500 + 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )
        cv2.putText(
            img_with_rect,
            f"fairy {rects_fairy}",
            (10, 500 + 150),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

    finally:
        print(f"Elapsed: {timer() - t} secs")
        print()

        cv2.imshow("img_with_rect " + file_name, img_with_rect)

        # cv2.imwrite(new_file_name, img_with_rect)
        # cv2.imwrite('img_with_rect.png', img_with_rect)

cv2.waitKey()
