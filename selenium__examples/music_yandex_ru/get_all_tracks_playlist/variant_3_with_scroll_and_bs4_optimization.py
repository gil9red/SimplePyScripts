#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
from timeit import default_timer

from bs4 import BeautifulSoup

# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    MoveTargetOutOfBoundsException,
    StaleElementReferenceException,
    TimeoutException,
)

from common import get_track, print_statistic, dump
from config import profile, options_headless, url, DIR_DUMP


DEBUG_LOG = False


t = default_timer()
data_by_track = dict()
i = 0

driver = None
try:
    driver = webdriver.Firefox(profile, options=options_headless)
    driver.implicitly_wait(2)  # seconds
    driver.get(url)
    print(f"Title: {driver.title!r}")

    time.sleep(5)

    footer_el = driver.find_element_by_class_name("footer")

    # Move down page to bottom
    y_position = 0
    while True:
        DEBUG_LOG and print("y_position:", y_position)
        try:
            ActionChains(driver).move_to_element(footer_el).perform()
            break
        except MoveTargetOutOfBoundsException:
            y_position += 250
            driver.execute_script(f"window.scrollTo(0, {y_position});")
            time.sleep(1)

        try:
            tracks_el = WebDriverWait(driver, timeout=5).until(
                EC.visibility_of_any_elements_located(
                    (By.CSS_SELECTOR, ".page-playlist__tracks-list .d-track")
                )
            )
        except (TimeoutException, StaleElementReferenceException):
            tracks_el = []

        for track_el in tracks_el:
            root = BeautifulSoup(track_el.get_attribute("outerHTML"), "html.parser")
            root = root.select_one(".d-track")

            data_b = root["data-b"]
            if data_b in data_by_track:
                continue

            track = get_track(track_el)

            i += 1
            DEBUG_LOG and print(
                f"{i}. {track.title}, {track_el.location}, {track_el.size}"
            )
            print(f"{i}. {track}")

            data_by_track[data_b] = track

        if tracks_el:
            track_el = tracks_el[-1]
            y_position = track_el.location["y"]
            DEBUG_LOG and print("Move y position last track:", y_position)
            driver.execute_script(f"window.scrollTo(0, {y_position});")
            time.sleep(1)

        time.sleep(0.1)

finally:
    if driver:
        driver.quit()

print("\n" + "-" * 100 + "\n")

print(f"Elapsed: {default_timer() - t:.2f} secs")

# Without list(...) there will be an error: ValueError: Circular reference detected
tracks = list(data_by_track.values())

print_statistic(tracks)
# Elapsed: 37.36 secs
# Total tracks: 421
# Total length: 26:01:11 (93671 secs)
#
# Unavailable tracks (11):
# ...

dump(tracks, DIR_DUMP / "variant_3.json")
