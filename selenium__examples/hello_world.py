#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# https://pypi.python.org/pypi/selenium


# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Если на этой строке исключение "Message: 'geckodriver' executable needs to be in PATH."
# Нужно:
#   * Из репозитория https://github.com/mozilla/geckodriver скачать geckodriver.exe
#   * Сохранить в папку, например: C:\Program Files\geckodriver\geckodriver.exe
#   * Добавить в системную переменную PATH путь к папке
driver = webdriver.Firefox()
driver.get('https://yahoo.com')
print('Title: "{}"'.format(driver.title))

search_box = driver.find_element_by_id('uh-search-box')
search_box.send_keys('Hello World!' + Keys.RETURN)

# Делаем скриншот результата
driver.save_screenshot('before_search.png')

try:
    elem = WebDriverWait(driver, timeout=10).until(EC.presence_of_element_located((By.ID, 'web')))

except TimeoutException:
    print('Timeout!')
    quit()

print('Title: "{}"'.format(driver.title))
elem.screenshot('search_content.png')

# Делаем скриншот результата
driver.save_screenshot('after_search.png')

driver.quit()
