#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os.path
import time
from pathlib import Path

# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


TOKEN = Path(__file__).resolve().parent / 'TOKEN'
LOGIN, PASSWORD = TOKEN.read_text().splitlines()


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


def open_web_page_water_meter(value_cold: int, value_hot: int) -> (bool, str):
    url = 'https://lk.erkc-info.ru/Input/InputData'

    value_cold = str(value_cold)
    value_hot = str(value_hot)

    driver = get_driver()
    driver.get(url)
    log.info(f'Title: {driver.title!r}')

    time.sleep(5)

    if '/Account/LogOn' in driver.current_url:
        log.info('Go auth')

        input_login = driver.find_element(By.ID, 'm_phone_log')
        input_login.send_keys(LOGIN)

        input_password = driver.find_element(By.ID, 'm_password_pas')
        input_password.send_keys(PASSWORD)

        while '/Account/LogOn' in driver.current_url:
            input_password.send_keys(Keys.RETURN)
            time.sleep(5)

        driver.get(url)

    input_cold = driver.find_element(By.ID, 'inputModel_InputCounters_0__newVal')
    input_cold.clear()
    input_cold.send_keys(value_cold)

    input_hot = driver.find_element(By.ID, 'inputModel_InputCounters_1__newVal')
    input_hot.clear()
    input_hot.send_keys(value_hot)

    return True, ''


if __name__ == '__main__':
    open_web_page_water_meter(123, 456)
