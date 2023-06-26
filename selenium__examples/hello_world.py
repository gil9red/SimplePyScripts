#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# https://pypi.python.org/pypi/selenium


# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#
# geckodriver: https://github.com/Mozilla/geckodriver/releases
#
# Если на этой строке исключение "Message: 'geckodriver' executable needs to be in PATH."
# Нужно:
#   * Из репозитория https://github.com/mozilla/geckodriver скачать geckodriver.exe
#   * Сохранить в папку, например: C:\Program Files\geckodriver\geckodriver.exe
#   * Добавить в системную переменную PATH путь к папке
#
# OR: driver = webdriver.Firefox(executable_path=r"C:\Program Files\geckodriver\geckodriver.exe")
driver = webdriver.Firefox()

try:
    driver.get("https://yahoo.com")
    print(f'Title: "{driver.title}"')

    search_box = driver.find_element(By.ID, "ybar-sbq")
    search_box.send_keys("Hello World!" + Keys.RETURN)

    # Делаем скриншот результата
    driver.save_screenshot("before_search.png")

    wait = WebDriverWait(driver, timeout=10)

    elem = wait.until(EC.presence_of_element_located((By.ID, "web")))
    elem.screenshot("search_content.png")

    print(f'Title: "{driver.title}"')

    # Делаем скриншот результата
    driver.save_screenshot("after_search.png")

finally:
    driver.quit()
