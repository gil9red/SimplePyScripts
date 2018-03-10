#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
driver.get('https://www.youtube.com/')
print('Title: "{}"'.format(driver.title))

# Делаем скриншот результата
driver.save_screenshot('before_search.png')

driver.find_element_by_css_selector('input#search').send_keys('Funny cats' + Keys.RETURN)

try:
    result_count = WebDriverWait(driver, timeout=10).until(EC.presence_of_element_located((By.ID, 'result-count')))
    print(result_count.text)

except TimeoutException:
    print('Timeout!')
    quit()

print('Title: "{}"'.format(driver.title))

# Делаем скриншот результата
driver.save_screenshot('after_search.png')

video_list = driver.find_elements_by_id('dismissable')

# Click on random video
import random
random.choice(video_list).click()

import time
time.sleep(10)

driver.save_screenshot('final.png')
