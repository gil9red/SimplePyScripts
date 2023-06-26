#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from bs4 import BeautifulSoup

# pip install selenium
from selenium import webdriver


url = "https://bash.im/byrating"

driver = webdriver.Firefox()
try:
    driver.implicitly_wait(2)
    driver.get(url)
    print(f"Title: {driver.title!r}\n")

    quote__header_el = driver.find_element_by_class_name("quote__header")

    outer_HTML = quote__header_el.get_attribute("outerHTML").strip()
    print(outer_HTML)
    # <header class="quote__header">
    #               <a class="quote__header_permalink" href="/quote/397136">#397136</a>
    #             <div class="quote__header_date">
    #         01.06.2008 в 21:26
    #       </div>
    #     </header>

    print("\n" + "-" * 100 + "\n")

    inner_HTML = quote__header_el.get_attribute("innerHTML").strip()
    print(inner_HTML)
    # <a class="quote__header_permalink" href="/quote/397136">#397136</a>
    #             <div class="quote__header_date">
    #         01.06.2008 в 21:26
    #       </div>

    print("\n" + "-" * 100 + "\n")

    root = BeautifulSoup(outer_HTML, "html.parser")
    print(root)
    # <header class="quote__header">
    # <a class="quote__header_permalink" href="/quote/397136">#397136</a>
    # <div class="quote__header_date">
    #         01.06.2008 в 21:26
    #       </div>
    # </header>

    print(root.select_one(".quote__header_permalink")["href"])
    # /quote/397136

finally:
    driver.quit()
