#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import random

# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


driver = webdriver.Firefox()
driver.implicitly_wait(10)  # seconds
driver.get("https://www.youtube.com/")
print(f'Title: "{driver.title}"')

# Делаем скриншот результата
driver.save_screenshot("before_search.png")

driver.find_element(By.CSS_SELECTOR, "input#search").send_keys(
    "Funny cats" + Keys.RETURN
)

result_count = driver.find_element(By.ID, "result-count")
print(result_count.text)

print(f'Title: "{driver.title}"')

# Делаем скриншот результата
driver.save_screenshot("after_search.png")

video_list = driver.find_elements(By.ID, "dismissable")

# Click on random video
random.choice(video_list).click()

video = WebDriverWait(driver, timeout=10).until(
    EC.visibility_of_element_located((By.TAG_NAME, "video"))
)

video_title = driver.find_element(By.CLASS_NAME, "title")
print(f'Title: "{driver.title}"')
print(f'Video Title: "{video_title.text}"')

driver.save_screenshot("final.png")

# driver.quit()
