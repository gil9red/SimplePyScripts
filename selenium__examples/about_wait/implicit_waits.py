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

driver = webdriver.Firefox()
driver.implicitly_wait(10)  # seconds
driver.get("https://www.youtube.com/")
print('Title: "{}"'.format(driver.title))

driver.find_element_by_css_selector("input#search").send_keys(
    "Funny cats" + Keys.RETURN
)

result_count = driver.find_element_by_id("result-count")
print(result_count.text)

print('Title: "{}"'.format(driver.title))

video_list = driver.find_elements_by_id("dismissable")

# Click on random video
random.choice(video_list).click()

video_title = driver.find_element_by_class_name("title")

# Bad algo, see explicit_waits.py
while True:
    if video_title.text:
        print('Title: "{}"'.format(driver.title))
        print('Video Title: "{}"'.format(video_title.text))
        break

    time.sleep(1)

driver.quit()
