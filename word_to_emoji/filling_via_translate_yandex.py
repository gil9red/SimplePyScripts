#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import time
import traceback

# pip install selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import db


URL = 'https://translate.yandex.ru/?lang=ru-emj&text='


driver = webdriver.Firefox()
driver.implicitly_wait(5)

try:
    for word in db.Word2Emoji.get_unprocessed_words():
        try:
            url = URL + word
            driver.get(url)
            print(f'Title: {driver.title!r}')

            while True:
                try:
                    emoji = driver.find_element_by_css_selector('#translation').text.strip()

                    # Перевод должен быть, если его нет, значит от сайта еще не пришел ответ
                    if not emoji:
                        time.sleep(2)
                        continue

                    print(f'Add {word!r} -> {emoji!r}')
                    db.Word2Emoji.add(word, emoji)
                    break

                # Иногда элемент не будет доступен, например при запросе капчи
                # Такие вещи нужно руками решать и пока они не решены, скрипт будет ожидать
                except (TimeoutException, NoSuchElementException):
                    time.sleep(10)

        except:
            print(traceback.format_exc())

        finally:
            time.sleep(5)

finally:
    driver.quit()
