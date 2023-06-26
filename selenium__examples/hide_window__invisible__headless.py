#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


options = Options()
options.add_argument("--headless")

driver = webdriver.Firefox(options=options)
driver.get("https://www.google.com/doodles")
print(f'Title: "{driver.title}"')

driver.quit()
