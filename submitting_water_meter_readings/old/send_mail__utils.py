#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os.path
import time
import random
from threading import Thread

# pip install selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


def get_logger(name=__file__):
    import logging
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(message)s')

    import sys
    sh = logging.StreamHandler(stream=sys.stdout)
    sh.setFormatter(formatter)
    log.addHandler(sh)

    return log


log = get_logger()


def get_driver(headless=False) -> webdriver.Firefox:
    if headless:
        options = Options()
        options.add_argument('--headless')
    else:
        options = None

    profile_directory = r'%AppData%\Mozilla\Firefox\Profiles\p75l82q1.for_mail__selenium'
    profile = webdriver.FirefoxProfile(os.path.expandvars(profile_directory))

    driver = webdriver.Firefox(profile, options=options)
    driver.implicitly_wait(20)  # seconds

    return driver


def open_web_page_mail(value_cold: int, value_hot: int) -> (bool, str):
    # Example: 123 -> 00123
    value_cold = str(value_cold).zfill(5)
    value_hot = str(value_hot).zfill(5)

    driver = get_driver()
    driver.get('https://e.mail.ru/templates/')
    log.info(f'Title: {driver.title!r}')

    items = [item for item in driver.find_elements_by_css_selector('a[href*="/templates/"]') if 'vodomer' in item.text]
    if not items:
        text = 'Шаблон с "vodomer" не найден'
        log.info(text)
        return False, text

    items[0].click()

    log.info(f'Title: {driver.title!r}')

    editor = driver.find_element(By.CSS_SELECTOR, '[role="textbox"]')
    template_text = editor.text

    if 'value_cold' not in template_text and 'value_hot' not in template_text:
        text = 'В шаблоне не найдены "value_cold" и "value_hot"'
        log.info(text)
        return False, text

    mail_text = template_text \
        .replace('value_cold', value_cold) \
        .replace('value_hot', value_hot)

    # Заполнение текста письма
    editor.clear()
    editor.send_keys(mail_text)

    return True, ''


def run_auto_ping_logon():
    prefix = run_auto_ping_logon.__name__

    def run():
        while True:
            try:
                driver = get_driver(headless=True)
                driver.get('https://e.mail.ru/inbox/')
                log.info(f'[{prefix}] Title: {driver.title!r}')

                driver.quit()

            except Exception as e:
                log.info(f'[{prefix}] Error: {e}')
                time.sleep(60)
                continue

            # Between 3 - 6 hours
            time.sleep(random.randint(3 * 3600, 6 * 3600))

    thread = Thread(target=run)
    thread.start()
