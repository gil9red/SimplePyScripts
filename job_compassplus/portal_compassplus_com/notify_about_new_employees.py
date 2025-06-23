#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
import traceback
import time

from urllib.parse import urljoin

import requests
from playwright.sync_api import sync_playwright, Page


URL_PORTAL: str = os.getenv("URL_PORTAL")
URL_NOTIFY: str = os.getenv("URL_NOTIFY")

if not URL_PORTAL:
    raise Exception("URL_PORTAL environment is not set!")

if not URL_NOTIFY:
    raise Exception("URL_NOTIFY environment variable is not set!")


def parse(page: Page, url_portal: str = URL_PORTAL, url_notify: str = URL_NOTIFY):
    print(f"Opening page: {url_portal}")
    page.goto(url_portal)

    css_selector = "a#NameFieldLink[href]"

    items = page.locator(css_selector).all()
    print("Users:", len(items))

    for user_el in items:
        url_mysite: str = user_el.get_attribute("href")
        username: str = url_mysite.rsplit("\\")[-1]

        full_name: str = user_el.text_content().strip()

        print(f"Check {full_name!r} ({username})")

        url_check: str = urljoin(url_notify, username)
        print(f"Sending a notification: {url_check}")

        rs = requests.get(url_check)
        rs.raise_for_status()

        # 201 вернется, если в ходе запроса был добавлен пользователь
        print(f"[{'+' if rs.status_code == 201 else '='}] {full_name!r} ({username})")
        print()


with sync_playwright() as p:
    print("Launching a browser")
    browser = p.firefox.launch()

    try:
        page = browser.new_page()

        max_attempts = 3
        attempt = 0
        while True:
            try:
                attempt += 1
                parse(page)
                break
            except Exception as e:
                print(f"#{attempt}.\n{traceback.format_exc()}")

                if attempt >= max_attempts:
                    raise e

                time.sleep(30)

    finally:
        browser.close()
