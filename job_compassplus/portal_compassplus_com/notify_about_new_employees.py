#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
from urllib.parse import urljoin

import requests
from playwright.sync_api import sync_playwright


URL_PORTAL: str = os.getenv("URL_PORTAL")
URL_NOTIFY: str = os.getenv("URL_NOTIFY")

if not URL_PORTAL:
    raise Exception("Переменная окружения URL_PORTAL не задана!")

if not URL_NOTIFY:
    raise Exception("Переменная окружения URL_NOTIFY не задана!")

with sync_playwright() as p:
    browser = p.firefox.launch()
    page = browser.new_page()

    rs = page.goto(URL_PORTAL)

    css_selector = "a#NameFieldLink[href]"

    for user_el in page.locator(css_selector).all():
        url_mysite: str = user_el.get_attribute("href")
        username: str = url_mysite.rsplit("\\")[-1]

        full_name: str = user_el.text_content().strip()

        print(f"Проверка {full_name!r} ({username})")

        url_check: str = urljoin(URL_NOTIFY, username)
        print(f"Отправка уведомления: {url_check}")
        print()

        rs = requests.get(url_check)
        rs.raise_for_status()

    browser.close()
