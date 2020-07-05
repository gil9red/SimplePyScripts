#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import time
import re
import sys

# pip install selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

sys.path.append('get_all_tracks_playlist')
from common import Track, get_track, seconds_to_str
from config import profile, url
from run_first_track import play_track


SEARCHING_TRACK = 'Шишки-телепаты'


driver = None
try:
    driver = webdriver.Firefox(profile)
    driver.implicitly_wait(2)
    driver.get(url)
    print(f'Title: {driver.title!r}')

    time.sleep(2)

    play_track(driver, SEARCHING_TRACK)

    progress__line__branding_el = driver.find_element_by_css_selector('.player-progress .progress__line__branding')

    while True:
        try:
            track_playing_el = driver.find_element_by_css_selector('.d-track_playing')
        except NoSuchElementException:
            continue

        track = get_track(track_playing_el)
        total_seconds = track.get_seconds()

        value = progress__line__branding_el.get_attribute('style')

        # Example: style="transform: translateX(-34.9234%);"
        m = re.search(r'translateX\((.+?)%\);', value)
        if m:
            progress_percent = 100 + float(m.group(1))
            progress_left = total_seconds * (progress_percent / 100)
            progress_left_str = seconds_to_str(progress_left)
            progress_right_str = seconds_to_str(total_seconds)
            print(f'{track.title}. {progress_left_str} / {progress_right_str} ({progress_percent:.1f}%)')

        time.sleep(1)

finally:
    if driver:
        driver.quit()
