#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


LOGIN = '<LOGIN>'
PASSWORD = '<PASSWORD>'


driver = webdriver.Firefox()
driver.implicitly_wait(10)

try:
    driver.get('https://www.avito.ru/')
    print(f'Title: "{driver.title}"')

    login_button_el = driver.find_element_by_css_selector('[data-marker="header/login-button"]')
    login_button_el.click()

    login_el = driver.find_element_by_css_selector('[data-marker="login-form/login"]')
    password_el = driver.find_element_by_css_selector('[data-marker="login-form/password"]')

    login_el.send_keys(LOGIN)
    password_el.send_keys(PASSWORD + Keys.RETURN)

    # NOTE: но останется проблема с капчей...
    #       можно оставить ее заполнение на человека, тогда скрипт
    #       должен ждать, когда человек введет капчу и закончит авторизацию,
    #       чтобы после уже самостоятельно работать с сайтом

finally:
    driver.quit()
