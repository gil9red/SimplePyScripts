#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://stackoverflow.com/a/29966769/5909792


# pip install selenium
from selenium import webdriver


USER_AGENT_MOBILE = "Mozilla/5.0 (Android 10; Mobile; rv:78.0) Gecko/78.0 Firefox/78.0"
url = "https://www.whatismybrowser.com/detect/what-is-my-user-agent"

driver = webdriver.Firefox()
try:
    driver.get(url)
    print(f"Title: {driver.title!r}\n")

    print("From js.   User-Agent:", driver.execute_script("return navigator.userAgent"))
    print("From site. User-Agent:", driver.find_element_by_id("detected_value").text)

finally:
    driver.quit()


print("\n" + "-" * 100 + "\n")

print("Change User-Agent on mobile")

profile = webdriver.FirefoxProfile()
profile.set_preference("general.useragent.override", USER_AGENT_MOBILE)

driver = webdriver.Firefox(profile)
try:
    driver.get(url)
    print(f"Title: {driver.title!r}\n")

    print("From js.   User-Agent:", driver.execute_script("return navigator.userAgent"))
    print("From site. User-Agent:", driver.find_element_by_id("detected_value").text)

finally:
    driver.quit()
