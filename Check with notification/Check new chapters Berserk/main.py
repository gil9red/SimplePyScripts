#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых главах Berserk.

"""


import sys
import time
import traceback

from typing import List

# pip install selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# Чтобы можно было импортировать all_common.py, находящийся уровнем выше
sys.path.append('..')
from all_common import make_backslashreplace_console, run_notification_job


make_backslashreplace_console()


def get_chapters() -> List[str]:
    URL = 'https://risens.team/title/28/berserk-manga/4333'

    options = Options()
    options.add_argument('--headless')

    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(5)
    try:
        driver.get(URL)
        print(f'Title: {driver.title!r}')

        time.sleep(5)

        driver.find_element_by_id('vs2__combobox').click()
        return [x.text for x in driver.find_elements_by_css_selector('ul#vs2__listbox > li')]

    except:
        print(traceback.format_exc())

    finally:
        driver.quit()

    return []


if __name__ == '__main__':
    run_notification_job(
        'Новые главы Berserk',
        'chapters',
        get_chapters,
        notified_by_sms=True,
        timeout={'days': 1},
        format_current_items='Текущий список глав (%s): %s',
        format_get_items='Запрос глав',
        format_items='Список глав (%s): %s',
        format_new_item='Новая глава "%s"',
        format_no_new_items='Изменений нет',
    )
