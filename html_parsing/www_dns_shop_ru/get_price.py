#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re

from http.cookies import SimpleCookie
from urllib.parse import urljoin

import requests

# pip install selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


session = requests.session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0"

PATTERN_PRICE = re.compile(r'"price":(\d+)')


def get_page_text(url: str) -> str | None:
    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)
    try:
        driver.implicitly_wait(20)
        driver.get(url)
        print(f"Title: {driver.title!r}")

        return driver.page_source

    except Exception as e:
        print(e)

    finally:
        driver.quit()

    return


def get_price(url: str) -> int | None:
    cookies = None
    attempts = 30

    while True:
        attempts -= 1
        if attempts <= 0:
            raise Exception("Too many redirects!")

        rs = session.get(url, allow_redirects=False, cookies=cookies)

        # TODO: bug fix (https://github.com/psf/requests/issues/5709)
        redirect_url = rs.headers.get("Location")
        if redirect_url:
            url = urljoin(rs.url, redirect_url)
            if rs.cookies:
                cookies = rs.cookies
                continue

            cookies = rs.headers.get("Set-Cookie")
            if cookies:
                cookies = {
                    key: value.value
                    for key, value in SimpleCookie(cookies).items()
                }

            continue

        break

    m = PATTERN_PRICE.search(rs.text)
    if not m:
        print("[#] Price not found from regex!")
        print("[+] Trying through selenium!")

        text = get_page_text(url)
        m = PATTERN_PRICE.search(text)
        if not m:
            print("[#] Price not found from regex [selenium]!")
            return

    price = int(m.group(1))

    # При отсутствии цены, значением у нее будет 0
    if price == 0:
        return

    return price


if __name__ == "__main__":
    for url in [
        "https://www.dns-shop.ru/product/4d664a0d90d61b80/processor-amd-ryzen-7-3700x-oem/",
        "https://technopoint.ru/product/4d664a0d90d61b80/processor-amd-ryzen-7-3700x-oem-sale/",
        "https://www.dns-shop.ru/product/8385e84a50f73332/operativnaa-pamat-neo-forza-encke-nmud416e82-3200dc20-32-gb/",
        "https://technopoint.ru/product/8385e84a50f73332/operativnaa-pamat-neo-forza-encke-nmud416e82-3200dc20-32-gb-sale/",
    ]:
        price = get_price(url)
        print(f"Price: {price}, url: {url}")

    # Price: 23299, url: https://www.dns-shop.ru/product/4d664a0d90d61b80/processor-amd-ryzen-7-3700x-oem/
    # Price: 22899, url: https://technopoint.ru/product/4d664a0d90d61b80/processor-amd-ryzen-7-3700x-oem-sale/
    # Price: 11299, url: https://www.dns-shop.ru/product/8385e84a50f73332/operativnaa-pamat-neo-forza-encke-nmud416e82-3200dc20-32-gb/
    # Price: 11099, url: https://technopoint.ru/product/8385e84a50f73332/operativnaa-pamat-neo-forza-encke-nmud416e82-3200dc20-32-gb-sale/
