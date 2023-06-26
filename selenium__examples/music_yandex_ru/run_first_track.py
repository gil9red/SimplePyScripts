#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
import sys

# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

sys.path.append("get_all_tracks_playlist")
from config import profile, url


def play_track(driver, track_title: str):
    try:
        tracks_el = WebDriverWait(driver, timeout=5).until(
            EC.visibility_of_any_elements_located(
                (By.CSS_SELECTOR, ".page-playlist__tracks-list .d-track")
            )
        )
    except TimeoutException:
        tracks_el = []

    track_el = None
    for x in tracks_el:
        title = x.find_element_by_css_selector(".d-track__title").text
        if title == track_title:
            track_el = x
            break

    if track_el:
        el = track_el.find_element_by_css_selector(".d-track__start-column")
        ActionChains(driver).move_to_element(el).click().perform()
    else:
        print(f"Not result for: {track_title!r}")

    return track_el


if __name__ == "__main__":
    driver = None
    try:
        driver = webdriver.Firefox(profile)
        driver.implicitly_wait(2)
        driver.get(url)
        print(f"Title: {driver.title!r}")

        time.sleep(2)

        SEARCHING_TRACK = "Шишки-телепаты"
        play_track(driver, SEARCHING_TRACK)

        # Чтобы скрипт завершился вместо с инстанцией селениума
        while True:
            _ = driver.title
            time.sleep(0.1)

    finally:
        if driver:
            driver.quit()
