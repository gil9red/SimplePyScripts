#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: http://selenium-python.readthedocs.io/waits.html
# Example:
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
# driver = webdriver.Firefox()
# driver.get("http://somedomain/url_that_delays_loading")
# try:
#     element = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.ID, "myDynamicElement"))
#     )
# finally:
#     driver.quit()


import random

# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
driver.get("https://www.youtube.com/")
print('Title: "{}"'.format(driver.title))

driver.find_element_by_css_selector("input#search").send_keys(
    "Funny cats" + Keys.RETURN
)

wait = WebDriverWait(driver, timeout=10)

result_count = wait.until(EC.presence_of_element_located((By.ID, "result-count")))
print(result_count.text)

print('Title: "{}"'.format(driver.title))

video_list = driver.find_elements_by_id("dismissable")

# Click on random video
random.choice(video_list).click()

video = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "video")))

video_title = driver.find_element_by_class_name("title")
print('Title: "{}"'.format(driver.title))
print('Video Title: "{}"'.format(video_title.text))

driver.quit()
