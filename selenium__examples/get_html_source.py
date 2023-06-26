#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install selenium
from selenium import webdriver


driver = webdriver.Firefox()
driver.get("https://www.youtube.com/")
print('Title: "{}"'.format(driver.title))

html = driver.page_source
print("Length:", len(html))
open("driver.page_source.html", "w").write(html)

driver.quit()
