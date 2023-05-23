#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as DT

from pathlib import Path

# pip install pandas
import pandas as pd

# pip install selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException


# TODO: Using WebDriverWait instead implicitly_wait
# TODO: Using logging instead print
# TODO: price must be decimal


def parse(url: str) -> list[tuple[str, str, str]]:
    options = Options()
    options.add_argument("--headless")

    items = []

    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(10)
    try:
        while True:
            print("Load:", url)
            driver.get(url)

            for item_el in driver.find_elements_by_css_selector(".goods-tile"):
                name = item_el.find_element_by_css_selector(".goods-tile__title").text

                # Не у всех товаров есть цена
                try:
                    price = item_el.find_element_by_css_selector(
                        ".goods-tile__price-value"
                    ).text
                except NoSuchElementException:
                    price = "-"

                nal = item_el.find_element_by_css_selector(
                    ".goods-tile__availability"
                ).text

                row = name, price, nal
                print(row)
                items.append(row)

            # Если есть кнопка перехода на следующую страницу, то продолжаем цикл, иначе завершаем
            try:
                a_next_page = driver.find_element_by_css_selector(
                    "a.pagination__direction_type_forward[href]"
                )
                url = a_next_page.get_attribute("href")

            except NoSuchElementException:
                break

    finally:
        driver.quit()

    return items


def save_goods(
    file_name: str | Path,
    items: list[tuple[str, str, str]],
    encoding="utf-8",
):
    df = pd.DataFrame(items, columns=["Name", "Price", "Nal"])
    df.to_csv(file_name, encoding=encoding)


if __name__ == "__main__":
    url = "https://rozetka.com.ua/search/?producer=gazer&seller=rozetka&text=Gazer"
    items = parse(url)
    print(f"Total goods: {len(items)}")

    file_name = f"rozetka_parser_{DT.datetime.now():%Y-%m-%d}.csv"
    print(f"Saved to {file_name}")
    save_goods(file_name, items)
