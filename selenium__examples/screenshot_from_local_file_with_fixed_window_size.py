#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
from pathlib import Path

# pip install selenium
from selenium import webdriver


file_name = "file_test.html"

driver = webdriver.Firefox()
driver.set_window_size(500, 500)
driver.get("file://" + str(Path(file_name).resolve()))

time.sleep(5)

driver.save_screenshot(file_name + ".png")

driver.quit()
