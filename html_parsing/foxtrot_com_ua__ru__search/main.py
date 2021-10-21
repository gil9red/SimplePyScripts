#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT
import time

from typing import List, Tuple, Union
from pathlib import Path

# pip install pandas
import pandas as pd

# pip install selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException


# TODO: Using logging instead print
# TODO: price must be decimal


def get_text_by_css(parent, css_selector: str, default: str) -> str:
    try:
        return parent.find_element_by_css_selector(css_selector).text
    except:
        return default


def parse(url_search: str) -> List[Tuple[str, str, str]]:
    options = Options()
    options.add_argument('--headless')

    items = []

    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(5.5)

    try:
        page = last_page = 1
        while page <= last_page:
            url = url_search
            if page > 1:
                url = f'{url_search}&page={page}'

            print(f'Load: {url}')
            driver.get(url)

            for item_el in driver.find_elements_by_css_selector(".card[data-url]"):
                name = get_text_by_css(item_el, '.card__title', 'Null')
                price = get_text_by_css(item_el, '.card-price', '-')
                nal = get_text_by_css(item_el, '.card__buttons', '-')

                row = name, price, nal
                print(row)

                items.append(row)

            # Обновление номера последней страницы
            try:
                pages_count_el = driver.find_element_by_css_selector('.listing__pagination[data-pages-count]')
                last_page = int(pages_count_el.get_attribute('data-pages-count'))

            except NoSuchElementException:
                break

            page += 1

    finally:
        driver.quit()

    return items



def save_goods(
        file_name: Union[str, Path],
        items: List[Tuple[str, str, str]],
        encoding='utf-8'
):
    df = pd.DataFrame(items, columns=['Name', 'Price', 'Nal'])
    df.to_csv(file_name, encoding=encoding)


if __name__ == '__main__':
    url = "https://www.foxtrot.com.ua/ru/search?query=gazer&filter=_195_588"
    items = parse(url)
    print(f'Total goods: {len(items)}')

    file_name = f'foxtrot_parser_{DT.datetime.now():%Y-%m-%d}.csv'
    print(f'Saved to {file_name}')
    save_goods(file_name, items)
