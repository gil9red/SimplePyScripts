#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install selenium
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService

# pip install webdriver-manager
from webdriver_manager.firefox import GeckoDriverManager


driver = webdriver.Firefox(
    service=FirefoxService(GeckoDriverManager().install()),
)
try:
    print("browserName:", driver.capabilities["browserName"])
    print("browserVersion:", driver.capabilities["browserVersion"])
    print("moz:geckodriverVersion:", driver.capabilities["moz:geckodriverVersion"])
    print("platformName:", driver.capabilities["platformName"])
    print("proxy:", driver.capabilities["proxy"])
    print("userAgent:", driver.capabilities["userAgent"])
    """
    browserName: firefox
    browserVersion: 129.0
    moz:geckodriverVersion: 0.35.0
    platformName: windows
    proxy: {}
    userAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0
    """
finally:
    driver.quit()
