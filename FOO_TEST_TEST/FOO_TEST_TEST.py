#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'ipetrash'


# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# # get the Firefox profile object
# firefox_profile = webdriver.FirefoxProfile()
#
# # Disable CSS
# firefox_profile.set_preference('permissions.default.stylesheet', 2)
#
# # Disable images
# firefox_profile.set_preference('permissions.default.image', 2)
#
# # Disable Flash
# firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
#
# driver = webdriver.Firefox(firefox_profile=firefox_profile)
driver = webdriver.Firefox()
driver.implicitly_wait(10)  # seconds
driver.get('https://pikabu.ru/story/ii_pobedil_5467581')
print('Title: "{}"'.format(driver.title))

i = 1
for img in driver.find_elements_by_css_selector('img[data-large-image]'):
    # print(img.get_attribute('src'), img.get_attribute('data-large-image'))
    print(i, img.get_attribute('data-large-image'))
    i += 1

# # Делаем скриншот результата
# driver.save_screenshot('before_search.png')
#
# driver.find_element_by_css_selector('input#search').send_keys('Funny cats' + Keys.RETURN)
#
# result_count = driver.find_element_by_id('result-count')
# print(result_count.text)
#
# print('Title: "{}"'.format(driver.title))
#
# # Делаем скриншот результата
# driver.save_screenshot('after_search.png')
#
# video_list = driver.find_elements_by_id('dismissable')
#
# # Click on random video
# import random
# random.choice(video_list).click()
#
# video = WebDriverWait(driver, timeout=10).until(
#     EC.visibility_of_element_located((By.TAG_NAME, 'video'))
# )
#
# video_title = driver.find_element_by_class_name('title')
# print('Title: "{}"'.format(driver.title))
# print('Video Title: "{}"'.format(video_title.text))
#
# driver.save_screenshot('final.png')

# driver.quit()
