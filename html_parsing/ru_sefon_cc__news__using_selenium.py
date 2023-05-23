#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import traceback

# pip install selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


URL = "https://ru.sefon.cc/news/"


options = Options()
options.add_argument("--headless")

driver = webdriver.Firefox(options=options)
try:
    driver.implicitly_wait(5)
    driver.get(URL)
    print(f"Title: {driver.title!r}")

    for a in driver.find_elements_by_css_selector(".mp3 > .btns > a[data-url]"):
        print(a.get_attribute("data-url"))

    # https://cdn5.sefon.pro/files/prev/193/Sontry%20-%20%D0%94%D0%B8%D1%81%D0%B1%D0%B0%D0%BB%D0%B0%D0%BD%D1%81%20%28192kbps%29.mp3
    # https://cdn5.sefon.pro/files/prev/193/Orlando%20-%20%D0%9D%D0%B5%20%D0%A1%D1%82%D0%B5%D1%81%D0%BD%D1%8F%D0%B9%D1%81%D1%8F%20%28192kbps%29.mp3
    # https://cdn8.sefon.pro/files/prev/193/%D0%A1%D0%B0%D1%88%D0%B0%20%D0%94%D0%B6%D0%B0%D0%B7%20-%20%D0%9F%D1%8C%D1%8F%D0%BD%D1%8B%D0%B9%20%D0%9F%D0%BE%20%D0%94%D0%B2%D0%BE%D1%80%D0%B0%D0%BC%20%28192kbps%29.mp3
    # https://cdn1.sefon.pro/files/prev/193/%D0%9E%D0%BA%D1%81%D0%B0%D0%BD%D0%B0%20%D0%9A%D0%BE%D0%B2%D0%B0%D0%BB%D0%B5%D0%B2%D1%81%D0%BA%D0%B0%D1%8F%20%26%20Andery%20Toronto%20-%20%D0%94%D0%B5%D0%B2%D0%BE%D1%87%D0%BA%D0%B0%20%D0%9D%D0%B5%20%D0%9F%D0%BB%D0%B0%D1%87%D1%8C%20%28192kbps%29.mp3
    # ...
    # https://cdn5.sefon.pro/files/prev/193/%D0%90%D1%80%D0%B8%D1%82%D0%BC%D0%B8%D1%8F%20feat.%20Lazy%20Cat%20-%20%D0%9A%D0%BE%D1%81%D0%BC%D0%BE%D1%81%20%28192kbps%29.mp3
    # https://cdn3.sefon.pro/files/prev/193/Delaney%20Jane%20-%20Want%20You%20Now%20%28192kbps%29.mp3
    # https://cdn8.sefon.pro/files/prev/193/%D0%9B%D0%B5%D0%B2%D0%B0%D0%BD%20%D0%93%D0%BE%D1%80%D0%BE%D0%B7%D0%B8%D1%8F%20-%20%D0%9F%D0%B0%D1%80%D0%BA%20%D0%93%D0%BE%D1%80%D1%8C%D0%BA%D0%BE%D0%B3%D0%BE%20%28192kbps%29.mp3
    # https://cdn6.sefon.pro/files/prev/193/Carlie%20Hanson%20-%20Good%20Enough%20%28192kbps%29.mp3

except:
    print(traceback.format_exc())

finally:
    driver.quit()
