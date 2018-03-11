#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://stackoverflow.com/a/42829700


# pip install selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
options = Options()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)
