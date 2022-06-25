#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import time
from typing import List

# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


URL = 'https://risens.team/title/28/berserk-manga/4333'


def get_chapters() -> List[str]:
    options = Options()
    options.add_argument('--headless')

    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(5)
    try:
        driver.get(URL)
        print(f'Title: {driver.title!r}')

        # Ожидание прогрузки страницы
        time.sleep(10)

        driver.find_element(By.ID, 'vs2__combobox').click()
        return [x.text for x in driver.find_elements(By.CSS_SELECTOR, 'ul#vs2__listbox > li')]

    finally:
        driver.quit()

    return []


if __name__ == '__main__':
    items = get_chapters()
    print(len(items))
    # 383
