#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# NOTE: Frozen Throne, 2560x1440


import time
import winsound

# pip install pyautogui
import pyautogui


LOCAL_NETWORK_BUTTON = 'images/local_network_button.png'
NEW_GAME_BUTTON = 'images/new_game_button.png'
NEW_GAME_BUTTON_SELECT_MAP = 'images/new_game_button_select_map.png'

OPEN_COMBO_BOX_SENTINEL = 'images/open_combo_box_sentinel.png'
OPEN_COMBO_BOX_SCOURGE = 'images/open_combo_box_scourge.png'


def go_local_network():
    pos = pyautogui.locateCenterOnScreen(LOCAL_NETWORK_BUTTON)
    print('LOCAL_NETWORK_BUTTON:', pos)

    if pos:
        pyautogui.click(pos)
        pyautogui.click(pos)

        winsound.Beep(1000, duration=10)
        return True

    return False


def go_new_game():
    pos = pyautogui.locateCenterOnScreen(NEW_GAME_BUTTON)
    print('NEW_GAME_BUTTON:', pos)

    if pos:
        pyautogui.click(pos)
        pyautogui.click(pos)

        winsound.Beep(1000, duration=10)
        return True

    return False


def go_select_map():
    pos = pyautogui.locateCenterOnScreen(NEW_GAME_BUTTON_SELECT_MAP)
    print('NEW_GAME_BUTTON_SELECT_MAP:', pos)

    if pos:
        pyautogui.click(pos)
        pyautogui.click(pos)

        winsound.Beep(1000, duration=10)
        return True

    return False


while True:
    # Кликаем на Локальную игру
    while not go_local_network():
        pass

    # Кликаем на Новую игру
    while not go_new_game():
        pass

    # Прогружается и выбирается последняя карта (нам она и нужна), кликаем на Новую игру
    while not go_select_map():
        pass

    #
    # Даем время прогрузиться
    #
    time.sleep(5)

    while True:
        #
        # Кликаем на игроков
        #
        coords_sentinel = list(pyautogui.locateAllOnScreen(OPEN_COMBO_BOX_SENTINEL))
        print('coords_sentinel:', coords_sentinel)

        coords_scourge = list(pyautogui.locateAllOnScreen(OPEN_COMBO_BOX_SCOURGE))
        print('coords_scourge:', coords_scourge)

        if coords_sentinel or coords_scourge:
            winsound.Beep(1000, duration=10)

            for rect in coords_sentinel + coords_scourge:
                pos = pyautogui.center(rect)

                # TODO: Научить бота выбирать соперника Легкий
                pyautogui.moveTo(pos)

                time.sleep(0.3)

            # pyautogui.moveTo(3000, 3000)
            # time.sleep(2)

            break

    time.sleep(1)
