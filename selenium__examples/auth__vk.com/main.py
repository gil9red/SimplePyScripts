#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

LOGIN = '<LOGIN>'
PASSWORD = '<PASSWORD>'

driver = webdriver.Firefox()
driver.get('https://vk.com/')
print('Title: "{}"'.format(driver.title))

index_email = driver.find_element_by_id('index_email')
index_email.send_keys(LOGIN)

index_pass = driver.find_element_by_id('index_pass')
index_pass.send_keys(PASSWORD)

# Делаем скриншот результата
driver.save_screenshot('before_auth.png')

driver.find_element_by_id("index_login_button").click()

try:
    profile_url = WebDriverWait(driver, timeout=10).until(EC.presence_of_element_located((By.ID, 'top_profile_link')))

except TimeoutException:
    print('Timeout!')
    quit()

print('Title: "{}"'.format(driver.title))
profile_url.click()

driver.find_element_by_id("top_profile_menu").screenshot('top_profile_menu.png')

# Click button my page
driver.find_element_by_id("top_myprofile_link").click()

try:
    page_info = WebDriverWait(driver, timeout=10).until(EC.presence_of_element_located((By.ID, 'page_info_wrap')))

except TimeoutException:
    print('Timeout!')
    quit()

print('Title: "{}"'.format(driver.title))
page_info.screenshot('page_info.png')

# Делаем скриншот результата
driver.save_screenshot('my_vk_user_page.png')

driver.quit()
