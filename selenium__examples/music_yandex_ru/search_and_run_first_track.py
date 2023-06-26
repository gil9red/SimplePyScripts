#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os.path

# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException


profile_directory = os.path.expandvars(
    r"%AppData%\Mozilla\Firefox\Profiles\p75l82q1.for_mail__selenium"
)
profile = webdriver.FirefoxProfile(profile_directory)

url = "https://music.yandex.ru/users/ilyapetrash/playlists/3"

driver = webdriver.Firefox(profile)
driver.implicitly_wait(2)
driver.get(url)
print(f"Title: {driver.title!r}")

SEARCHING_TRACK = "Шишки-телепаты"

search_el = WebDriverWait(driver, timeout=5).until(
    EC.visibility_of_element_located(
        (By.CSS_SELECTOR, ".playlist-filter-suggest input[type=text]")
    )
)
ActionChains(driver).move_to_element(search_el).click().send_keys(
    SEARCHING_TRACK
).perform()

# Кликаем на поиск пока не будет выполнен поиск и не появится результат
while True:
    search_el.send_keys(Keys.RETURN)
    try:
        playlist_filter_suggest_el = WebDriverWait(driver, timeout=1).until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "playlist-filter-suggest__result")
            )
        )
        break
    except TimeoutException:
        pass

# Проверяем наличие треков после поиска
try:
    tracks_el = WebDriverWait(driver, timeout=1).until(
        EC.visibility_of_any_elements_located(
            (
                By.CSS_SELECTOR,
                ".playlist-filter-suggest__result [data-card=filtered] > .d-track",
            )
        )
    )
except TimeoutException:
    tracks_el = []

if tracks_el:
    el = tracks_el[0].find_element_by_css_selector(".d-track__start-column")
    ActionChains(driver).move_to_element(el).click().perform()
else:
    print(f"Not result for: {SEARCHING_TRACK!r}")
