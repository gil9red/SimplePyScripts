#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install selenium
from selenium import webdriver


# get the Firefox profile object
firefox_profile = webdriver.FirefoxProfile()

# Disable CSS
firefox_profile.set_preference("permissions.default.stylesheet", 2)

# Disable images
firefox_profile.set_preference("permissions.default.image", 2)

# Disable Flash
firefox_profile.set_preference("dom.ipc.plugins.enabled.libflashplayer.so", "false")

driver = webdriver.Firefox(firefox_profile=firefox_profile)
driver.implicitly_wait(10)  # seconds
driver.get("https://pikabu.ru/story/ii_pobedil_5467581")
print('Title: "{}"'.format(driver.title))
