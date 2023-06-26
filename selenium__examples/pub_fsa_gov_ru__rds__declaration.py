#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Firefox()
driver.implicitly_wait(10)
driver.get("https://pub.fsa.gov.ru/rds/declaration")

content = driver.find_element(By.CSS_SELECTOR, "input[_ngcontent-c27]")
content.send_keys("ЕАЭС N RU Д-TR.РА01.А.44855/19")
