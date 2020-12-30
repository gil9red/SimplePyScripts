#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import time

# pip install selenium
from selenium import webdriver


driver = webdriver.Firefox()
driver.implicitly_wait(10)

try:
    driver.get('https://yahoo.com')
    print(f'Title: "{driver.title}"')

    # Opens a new tab
    driver.execute_script("window.open()")

    print('Tabs:', len(driver.window_handles), driver.window_handles)

    driver.switch_to.window(driver.window_handles[1])

    time.sleep(2)

    driver.switch_to.window(driver.window_handles[0])

    time.sleep(2)

finally:
    driver.quit()
