#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time

# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

from config import LOGIN, PASSWORD


URL = "https://mail.compassplus.com"

driver = webdriver.Firefox()

try:
    driver.implicitly_wait(10)  # seconds
    driver.get(URL)
    print(f'Title: "{driver.title}"')

    driver.find_element(By.ID, "username").send_keys(LOGIN)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)

    # Делаем скриншот результата
    driver.save_screenshot("before_auth.png")

    driver.find_element(By.CLASS_NAME, "signinbutton").click()

    driver.save_screenshot("after_auth.png")
    print(f'Title: "{driver.title}"')

    driver.save_screenshot("before_click_on_calendar.png")
    print(f'Title: "{driver.title}"')

    html = driver.page_source
    print("Length:", len(html))
    open("driver.before_click_on_calendar.html", "w", encoding="utf-8").write(html)

    # Ждем и кликаем на кнопку
    driver.find_element(By.XPATH, '//*[text()="Календарь"]').click()

    html = driver.page_source
    print("Length:", len(html))
    open("driver.after_click_on_calendar.html", "w", encoding="utf-8").write(html)

    driver.save_screenshot("after_click_on_calendar.png")
    print(f'Title: "{driver.title}"')

    # Ждем пока появится элемент
    driver.find_element(By.CSS_SELECTOR, '[aria-label="Представление календаря"]')

    # Даем еще время на прогрузку календаря
    time.sleep(10)

    html = driver.page_source
    print("Length:", len(html))
    open("driver.after_click_on_calendar_2.html", "w", encoding="utf-8").write(html)

    driver.save_screenshot("after_click_on_calendar_2.png")
    print(f'Title: "{driver.title}"')

    # TODO: нужно

finally:
    # TODO:
    # driver.quit()
    pass
