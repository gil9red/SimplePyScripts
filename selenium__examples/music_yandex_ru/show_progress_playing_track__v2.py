#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
import sys

from bs4 import BeautifulSoup

# pip install selenium
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)

sys.path.append("get_all_tracks_playlist")
from common import Track, get_track, seconds_to_str
from config import profile, url
from run_first_track import play_track


def to_seconds(time_str: str) -> int:
    if not time_str:
        return 0

    parts = time_str.split(":")
    if len(parts) != 2:
        return 0
    return int(parts[0]) * 60 + int(parts[1])


SEARCHING_TRACK = "Шишки-телепаты"


driver = None
try:
    # Mute
    profile.set_preference("media.volume_scale", "0.0")

    driver = webdriver.Firefox(profile)
    driver.implicitly_wait(2)
    driver.get(url)
    print(f"Title: {driver.title!r}")

    time.sleep(2)

    play_track(driver, SEARCHING_TRACK)

    player_progress_el = driver.find_element_by_css_selector(".player-progress")
    progress__text_el = player_progress_el.find_element_by_css_selector(
        ".progress__bar.progress__text"
    )

    while True:
        try:
            track_playing_el = driver.find_element_by_css_selector(".d-track_playing")
            track = get_track(track_playing_el)
        except (NoSuchElementException, StaleElementReferenceException):
            continue

        el_html = progress__text_el.get_attribute("outerHTML")
        root = BeautifulSoup(el_html, "html.parser")

        progress_left = to_seconds(root.select_one(".progress__left").text)
        progress_right = to_seconds(root.select_one(".progress__right").text)
        if progress_right == 0:
            continue

        progress_left_str = seconds_to_str(progress_left)
        progress_right_str = seconds_to_str(progress_right)

        print(
            f"{track.title}. {progress_left_str} / {progress_right_str} ({progress_left / progress_right:.1%})"
        )

        time.sleep(1)

finally:
    if driver:
        driver.quit()
