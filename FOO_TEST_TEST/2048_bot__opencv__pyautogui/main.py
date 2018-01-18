#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'ipetrash'


import cv2
import numpy as np
import pyautogui
import time

import utils

# TODO: append logger
# TODO: проверить опции:
#     # speed-up using multithreads
#     cv2.setUseOptimized(True)
#     cv2.setNumThreads(4)

while True:
    try:
        pil_image = pyautogui.screenshot()

        # Появляется кнопка при получении ячейки 2048
        pos = utils.locate_center_on_screen('button/continue.png', pil_image)
        if pos:
            # Клик на кнопку и ожидание
            pyautogui.click(pos, pause=5)

        # Появляется кнопка при проигрыше
        pos = utils.locate_center_on_screen('button/play_again.png', pil_image)
        if pos:
            utils.make_screenshot()

            # Клик на кнопку и ожидание
            pyautogui.click(pos, pause=5)

        opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        board_img = utils.get_game_board(opencv_image)
        if board_img is None:
            time.sleep(1)
            continue

        value_matrix = utils.get_value_matrix_from_board(board_img)
        print('value_matrix:', value_matrix)

        next_move = utils.get_next_move(value_matrix)
        print('next_move:', next_move)

        # Посылаем нужный клик на стрелки
        pyautogui.typewrite([next_move])

    except Exception as e:
        print('Error:', e)

        utils.make_screenshot()

    finally:
        time.sleep(1)
