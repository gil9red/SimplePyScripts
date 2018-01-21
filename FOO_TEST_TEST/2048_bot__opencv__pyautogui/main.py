#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'ipetrash'


import cv2
import numpy as np
import pyautogui
import time

import utils
log = utils.log


BUTTON_CONTINUE = 'button/continue.png'
BUTTON_PLAY_AGAIN = 'button/play_again.png'

# TODO: проверить опции:
# # Speed-up using multithreads
# cv2.setUseOptimized(True)
# cv2.setNumThreads(4)

while True:
    t = time.clock()

    try:
        log.debug('Start')

        pil_image = pyautogui.screenshot()
        log.debug('Get screenshot: %s', pil_image)

        # Появляется кнопка при получении ячейки 2048
        pos = utils.locate_center_on_screen(BUTTON_CONTINUE, pil_image)
        if pos:
            log.debug('Found BUTTON_CONTINUE, pos: %s', pos)

            # Клик на кнопку и ожидание
            pyautogui.click(pos, pause=10)

        # Появляется кнопка при проигрыше
        pos = utils.locate_center_on_screen(BUTTON_PLAY_AGAIN, pil_image)
        if pos:
            log.debug('Found BUTTON_PLAY_AGAIN, pos: %s', pos)

            utils.make_screenshot(prefix='end_game__')

            # Клик на кнопку и ожидание
            pyautogui.click(pos, pause=10)

        pil_image = pyautogui.screenshot()
        # log.debug('Get screenshot: %s', pil_image)

        opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        board_img = utils.get_game_board(opencv_image)
        log.debug('Found board: %s', board_img.shape[:2])

        value_matrix = utils.get_value_matrix_from_board(board_img)
        # log.debug('value_matrix: %s', value_matrix)

        next_move = utils.get_next_move(value_matrix)
        log.debug('next_move: %s', next_move)

        # Посылаем нужный клик на стрелки
        pyautogui.typewrite([next_move], pause=2)

    except utils.NotFoundItem as e:
        log.info(e)

        time.sleep(5)

    except Exception as e:
        utils.make_screenshot(prefix='error__')

        log.exception('Ошибка:')
        log.debug('Через 5 минут попробую снова...')

        time.sleep(5 * 60)

    finally:
        log.debug('Finish. Elapsed time: %s secs', time.clock() - t)
