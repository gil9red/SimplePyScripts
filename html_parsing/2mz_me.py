#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


options = Options()
options.add_argument("--headless")

driver = webdriver.Firefox(options=options)
driver.implicitly_wait(10)

try:
    driver.get("https://2mz.me/")
    print(f'Title: "{driver.title}"')

    for item in driver.find_elements(By.CSS_SELECTOR, "#tracks .item"):
        title = item.find_element(By.CSS_SELECTOR, ".item-title").text
        author = item.find_element(By.CSS_SELECTOR, ".item-author").text
        print(title, author)

finally:
    driver.quit()
