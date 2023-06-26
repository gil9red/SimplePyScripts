#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install selenium
from selenium import webdriver


driver = webdriver.Firefox()
driver.implicitly_wait(10)
driver.get("https://pub.fsa.gov.ru/rds/declaration")

content = driver.find_element_by_css_selector("input[_ngcontent-c27]")
content.send_keys("ЕАЭС N RU Д-TR.РА01.А.44855/19")
