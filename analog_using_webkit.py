#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""Использование selenium для загрузки и получения страницы с javascript."""


from bs4 import BeautifulSoup
from operator import itemgetter
from selenium import webdriver


url = "http://www.oddsportal.com/soccer/england/premier-league/everton-arsenal-tnWxil2o#over-under;2"
browser = webdriver.Firefox()

browser.get(url)
soup = BeautifulSoup(browser.page_source)
data_table = soup.find("div", {"id": "odds-data-table"})

for div in data_table.find_all_next("div", attrs={"class=": "table-container"}):
    row = div.find_all(["span", "strong"])

    if len(row):
        print(
            ",".join(
                cell.get_text(strip=True) for cell in itemgetter(0, 4, 3, 2, 1)(row)
            )
        )
