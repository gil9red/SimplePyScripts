#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# NOTE: Frozen Throne, 2560x1440


import time
# import winsound

# pip install pyautogui
import pyautogui


LOCAL_NETWORK_BUTTON = 'images/local_network_button.png'
NEW_GAME_BUTTON = 'images/new_game_button.png'
NEW_GAME_BUTTON_SELECT_MAP = 'images/new_game_button_select_map.png'

OPEN_COMBO_BOX_SENTINEL = 'images/open_combo_box_sentinel.png'
OPEN_COMBO_BOX_SCOURGE = 'images/open_combo_box_scourge.png'

SELECT_AI_MENU_SENTINEL = "images/select_ai_menu_sentinel.png"
SELECT_AI_MENU_SCOURGE = "images/select_ai_menu_scourge.png"
AI_EASY = "images/ai_easy.png"


def go_local_network():
    pos = pyautogui.locateCenterOnScreen(LOCAL_NETWORK_BUTTON)
    print('LOCAL_NETWORK_BUTTON:', pos)

    if pos:
        pyautogui.click(pos)
        pyautogui.click(pos)

        # winsound.Beep(1000, duration=10)
        return True

    return False


def go_new_game():
    pos = pyautogui.locateCenterOnScreen(NEW_GAME_BUTTON)
    print('NEW_GAME_BUTTON:', pos)

    if pos:
        pyautogui.click(pos)
        pyautogui.click(pos)

        # winsound.Beep(1000, duration=10)
        return True

    return False


def go_select_map():
    pos = pyautogui.locateCenterOnScreen(NEW_GAME_BUTTON_SELECT_MAP)
    print('NEW_GAME_BUTTON_SELECT_MAP:', pos)

    if pos:
        pyautogui.click(pos)
        pyautogui.click(pos)

        # winsound.Beep(1000, duration=10)
        return True

    return False


def bot_says():
    text = """\
Bot version: 1.0
-aremnpakulsc

    """

    for line in text.splitlines():
        pyautogui.typewrite(line)
        pyautogui.typewrite(['enter'])


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
        coords_scourge = list(pyautogui.locateAllOnScreen(OPEN_COMBO_BOX_SCOURGE))
        print(f'coords_sentinel: {coords_sentinel}, coords_scourge: {coords_scourge}')

        if coords_sentinel and coords_scourge:
            bot_says()

            # Освобождаем место для первого игрока
            coords_sentinel.pop(0)

            # winsound.Beep(1000, duration=10)

            for rect in coords_sentinel + coords_scourge:
                pos = pyautogui.center(rect)

                while True:
                    # Клием на комбобокс
                    pyautogui.moveTo(pos) or time.sleep(0.3)
                    pyautogui.click(pos)
                    time.sleep(0.3)

                    # Ждем появления меню
                    pos_menu_sentinel = pyautogui.locateCenterOnScreen(SELECT_AI_MENU_SENTINEL)
                    pos_menu_scourge = pyautogui.locateCenterOnScreen(SELECT_AI_MENU_SCOURGE)
                    print(f'SELECT_AI_MENU_SENTINEL: {pos_menu_sentinel}, SELECT_AI_MENU_SCOURGE: {pos_menu_scourge}')

                    if pos_menu_sentinel or pos_menu_scourge:
                        break

                # Выбираем игрока
                pos = pyautogui.locateCenterOnScreen(AI_EASY)
                print('AI_EASY:', pos)
                if pos:
                    pyautogui.moveTo(pos) or time.sleep(0.3)
                    pyautogui.click(pos)

                time.sleep(0.3)

            break

        time.sleep(1)

    time.sleep(1)
