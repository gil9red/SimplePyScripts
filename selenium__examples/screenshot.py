#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time

# pip install selenium
from selenium import webdriver


driver = webdriver.Firefox()
driver.get("https://www.youtube.com/")
print('Title: "{}"'.format(driver.title))

time.sleep(5)

driver.save_screenshot("screenshot.png")

driver.quit()
