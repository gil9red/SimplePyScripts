#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os.path

# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


profile_directory = os.path.expandvars(r'%AppData%\Mozilla\Firefox\Profiles\p75l82q1.for_mail__selenium')
profile = webdriver.FirefoxProfile(profile_directory)

url = 'https://music.yandex.ru/users/ilyapetrash/playlists/3'

driver = webdriver.Firefox(profile)
driver.implicitly_wait(2)
driver.get(url)
print(f'Title: {driver.title!r}')

SEARCHING_TRACK = 'Шишки-телепаты'

try:
    tracks_el = WebDriverWait(driver, timeout=5).until(
        EC.visibility_of_any_elements_located(
            (By.CSS_SELECTOR, '.page-playlist__tracks-list .d-track')
        )
    )
except TimeoutException:
    tracks_el = []

track_el = None
for x in tracks_el:
    title = x.find_element_by_css_selector('.d-track__title').text
    if title == SEARCHING_TRACK:
        track_el = x
        break

if track_el:
    el = track_el.find_element_by_css_selector('.d-track__start-column')
    ActionChains(driver).move_to_element(el).click().perform()
else:
    print(f'Not result for: {SEARCHING_TRACK!r}')
