#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time

# pip install selenium
from selenium import webdriver


driver = webdriver.Firefox()
driver.set_window_size(500, 500)
driver.get("https://www.youtube.com/")
print(f'Title: "{driver.title}"')

time.sleep(5)

driver.save_screenshot("screenshot.png")

driver.quit()
