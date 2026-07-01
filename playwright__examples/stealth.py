#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path

from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

DIR: Path = Path(__file__).resolve().parent
DIR_SCREENSHOTS: Path = DIR / "screenshots" / "stealth"
DIR_SCREENSHOTS.mkdir(parents=True, exist_ok=True)

URL: str = "https://bot.sannysoft.com/"

stealth = Stealth()


with sync_playwright() as p:
    for browser_type in [p.chromium, p.firefox, p.webkit]:
        print(browser_type.name)

        browser = browser_type.launch()
        page = browser.new_page()

        page.goto(URL)
        print("navigator.webdriver (default):", page.evaluate("navigator.webdriver"))

        normal_screenshot_path: Path = (
            DIR_SCREENSHOTS / f"normal_{browser_type.name}_page.png"
        )
        page.screenshot(path=normal_screenshot_path)

        stealth.apply_stealth_sync(page)
        page.goto(URL)
        print("navigator.webdriver (stealth):", page.evaluate("navigator.webdriver"))

        stealth_screenshot_path: Path = (
            DIR_SCREENSHOTS / f"stealth_{browser_type.name}_page.png"
        )
        page.screenshot(path=stealth_screenshot_path)

        browser.close()  # NOTE: Close in loop
        print()

"""
chromium
navigator.webdriver (default): True
navigator.webdriver (stealth): False

firefox
navigator.webdriver (default): True
navigator.webdriver (stealth): False

webkit
navigator.webdriver (default): True
navigator.webdriver (stealth): False
"""
