#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://ru.stackoverflow.com/a/745919


from time import sleep

# pip install pyperclip
import pyperclip

# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


# Открываем и копируем содержимое файла
with open(__file__, encoding="utf-8") as f:
    text = f.read()
    pyperclip.copy(text)

driver = webdriver.Firefox()
driver.get("https://pastebin.com/")

# Вставляем текст с буфера обмена
driver.find_element(By.ID, "paste_code").send_keys(Keys.CONTROL + "v")

# sleep для того чтобы увидеть результат, перед тем как будет
# вызван driver.quit(), который закроет окно браузера
sleep(5)

driver.quit()
