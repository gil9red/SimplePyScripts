#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

LOGIN = '<LOGIN>'
PASSWORD = '<PASSWORD>'

driver = webdriver.Firefox()
driver.get('https://vk.com/')
print('Title: "{}"'.format(driver.title))

driver.find_element_by_id('index_email').send_keys(LOGIN)
driver.find_element_by_id('index_pass').send_keys(PASSWORD)

# Делаем скриншот результата
driver.save_screenshot('before_auth.png')

driver.find_element_by_id("index_login_button").click()

try:
    l_msg = WebDriverWait(driver, timeout=10).until(EC.presence_of_element_located((By.ID, 'l_msg')))

except TimeoutException:
    print('Timeout!')
    quit()

print('Title: "{}"'.format(driver.title))

# Делаем скриншот результата
driver.save_screenshot('after_auth.png')

l_msg.click()

try:
    im_dialogs = WebDriverWait(driver, timeout=10).until(EC.presence_of_element_located((By.ID, 'im_dialogs')))
    im_dialogs.screenshot('dialogs_page.png')

except TimeoutException:
    print('Timeout!')
    quit()

print('Title: "{}"'.format(driver.title))

dialog_items = driver.find_elements_by_class_name('_im_dialog_link')

for dialog in dialog_items:
    print(dialog.text)

driver.quit()
