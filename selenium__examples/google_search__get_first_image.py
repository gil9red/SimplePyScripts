#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from base64 import b64decode

# pip install selenium
from selenium import webdriver


key = "яблоко"
url = (
    f"https://www.google.ru/search?q={key}&newwindow=1&espv=2&source=lnms&tbm=isch&sa=X"
)

driver = webdriver.Firefox()
driver.implicitly_wait(10)  # seconds
driver.get(url)

# Поиск первой картинки
img = driver.find_element_by_xpath(
    '//img[starts-with(@src, "data:image/jpeg;base64,")]'
)

src = img.get_attribute("src")
src = src.split("data:image/jpeg;base64,")[1]

img_data = b64decode(src)

with open("img.jpg", "wb") as f:
    f.write(img_data)

# Делаем скриншот результата
driver.save_screenshot("screenshot.png")

driver.quit()
