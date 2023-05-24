#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
import traceback

# pip install selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


URL = "https://www.s7.ru/"


options = Options()
options.add_argument("--headless")

driver = webdriver.Firefox(options=options)
try:
    driver.implicitly_wait(5)
    driver.get(URL)
    print(f"Title: {driver.title!r}")

    # Заметил, что без дополнительного ожидания у <from_el> не весь текст
    time.sleep(10)

    for item in driver.find_elements_by_css_selector(".special-offers__item"):
        to_el = item.find_element_by_css_selector(".special-offers__to")
        from_el = item.find_element_by_css_selector(".special-offers__from")
        price_el = item.find_element_by_css_selector(".special-offers__price")

        print(f"{to_el.text:15} | {from_el.text} | {price_el.text}")

    """
    Новосибирск     | из Магнитогорска, туда и обратно | от 12 200 ₽
    Москва          | из Магнитогорска, туда и обратно | от 18 681 ₽
    Казань          | из Магнитогорска, туда и обратно | Проверить цену
    Красноярск      | из Магнитогорска, туда и обратно | Проверить цену
    Мирный          | из Магнитогорска, туда и обратно | Проверить цену
    Норильск        | из Магнитогорска, туда и обратно | Проверить цену
    """

except:
    print(traceback.format_exc())

finally:
    driver.quit()
