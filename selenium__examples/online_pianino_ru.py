#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time

# pip install selenium
from selenium import webdriver


driver = webdriver.Firefox()
driver.implicitly_wait(20)  # seconds
driver.get("https://online-pianino.ru/")
print(f"Title: {driver.title!r}")

for button in driver.find_elements_by_css_selector("#keyboardspot button[id]"):
    print(button.get_attribute("id"))
    button.click()

    time.sleep(0.3)
