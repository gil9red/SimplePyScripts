#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path
from playwright.sync_api import sync_playwright

DIR: Path = Path(__file__).resolve().parent
DIR_SCREENSHOTS: Path = DIR / "screenshots"
DIR_SCREENSHOTS.mkdir(parents=True, exist_ok=True)


with sync_playwright() as p:
    for browser_type in [p.chromium, p.firefox, p.webkit]:
        print(browser_type.name)

        browser = browser_type.launch()
        page = browser.new_page()

        page.goto("https://github.com/gil9red")

        path_page: Path = DIR_SCREENSHOTS / f"{browser_type.name}_page.png"
        page.screenshot(path=path_page)

        path_full_page: Path = DIR_SCREENSHOTS / f"{browser_type.name}_full_page.png"
        page.screenshot(path=path_full_page, full_page=True)
