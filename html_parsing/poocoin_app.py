#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import traceback

# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.by import By


URL = "https://poocoin.app/tokens/0x2a69c59b8b493141d9f41b8f4fa724b60cd204e0"

driver = webdriver.Firefox()
try:
    driver.implicitly_wait(5)
    driver.get(URL)
    print(f"Title: {driver.title!r}")

    token_price = driver.find_element(
        By.CSS_SELECTOR, ".mb-1.d-flex.flex-column.lh-1 > .text-success"
    )
    print(token_price.text)
    # $0.00165060

except:
    print(traceback.format_exc())

finally:
    driver.quit()
