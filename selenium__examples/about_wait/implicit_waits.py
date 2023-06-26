#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: http://selenium-python.readthedocs.io/waits.html
# Example:
# from selenium import webdriver
#
# driver = webdriver.Firefox()
# driver.implicitly_wait(10) # seconds
# driver.get("http://somedomain/url_that_delays_loading")
# myDynamicElement = driver.find_element_by_id("myDynamicElement")


import random
import time

# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


driver = webdriver.Firefox()
driver.implicitly_wait(10)  # seconds
driver.get("https://www.youtube.com/")
print(f'Title: "{driver.title}"')

driver.find_element(By.CSS_SELECTOR, "input#search").send_keys(
    "Funny cats" + Keys.RETURN
)

result_count = driver.find_element(By.ID, "result-count")
print(result_count.text)

print(f'Title: "{driver.title}"')

video_list = driver.find_elements(By.ID, "dismissable")

# Click on random video
random.choice(video_list).click()

video_title = driver.find_element(By.CLASS_NAME, "title")

# Bad algo, see explicit_waits.py
while True:
    if video_title.text:
        print(f'Title: "{driver.title}"')
        print(f'Video Title: "{video_title.text}"')
        break

    time.sleep(1)

driver.quit()
