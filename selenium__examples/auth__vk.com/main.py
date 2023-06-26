#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


LOGIN = "<LOGIN>"
PASSWORD = "<PASSWORD>"

driver = webdriver.Firefox()
driver.get("https://vk.com/")
print(f'Title: "{driver.title}"')

driver.find_element_by_id("index_email").send_keys(LOGIN)
driver.find_element_by_id("index_pass").send_keys(PASSWORD)

# Делаем скриншот результата
driver.save_screenshot("before_auth.png")

driver.find_element_by_id("index_login_button").click()

wait = WebDriverWait(driver, timeout=10)

profile_url = wait.until(EC.presence_of_element_located((By.ID, "top_profile_link")))
print(f'Title: "{driver.title}"')
profile_url.click()

driver.find_element_by_id("top_profile_menu").screenshot("top_profile_menu.png")

# Click button my page
driver.find_element_by_id("top_myprofile_link").click()

page_info = wait.until(EC.presence_of_element_located((By.ID, "page_info_wrap")))
page_info.screenshot("page_info.png")

print(f'Title: "{driver.title}"')

# Делаем скриншот результата
driver.save_screenshot("my_vk_user_page.png")

driver.quit()
