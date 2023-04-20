#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time

# pip install selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from config import LOGIN, PASSWORD


URL = "https://mail.compassplus.com"

driver = webdriver.Firefox()

try:
    driver.implicitly_wait(10)  # seconds
    driver.get(URL)
    print('Title: "{}"'.format(driver.title))

    driver.find_element_by_id("username").send_keys(LOGIN)
    driver.find_element_by_id("password").send_keys(PASSWORD)

    # Делаем скриншот результата
    driver.save_screenshot("before_auth.png")

    driver.find_element_by_class_name("signinbutton").click()

    driver.save_screenshot("after_auth.png")
    print('Title: "{}"'.format(driver.title))

    driver.save_screenshot("before_click_on_calendar.png")
    print('Title: "{}"'.format(driver.title))

    html = driver.page_source
    print("Length:", len(html))
    open("driver.before_click_on_calendar.html", "w", encoding="utf-8").write(html)

    # Ждем и кликаем на кнопку
    driver.find_element_by_xpath('//*[text()="Календарь"]').click()

    html = driver.page_source
    print("Length:", len(html))
    open("driver.after_click_on_calendar.html", "w", encoding="utf-8").write(html)

    driver.save_screenshot("after_click_on_calendar.png")
    print('Title: "{}"'.format(driver.title))

    # Ждем пока появится элемент
    driver.find_element_by_css_selector('[aria-label="Представление календаря"]')

    # Даем еще время на прогрузку календаря
    time.sleep(10)

    html = driver.page_source
    print("Length:", len(html))
    open("driver.after_click_on_calendar_2.html", "w", encoding="utf-8").write(html)

    driver.save_screenshot("after_click_on_calendar_2.png")
    print('Title: "{}"'.format(driver.title))

    # TODO: нужно

finally:
    # TODO:
    # driver.quit()
    pass
