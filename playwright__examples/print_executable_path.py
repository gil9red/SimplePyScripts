#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    for browser_type in [p.chromium, p.firefox, p.webkit]:
        print(browser_type.name, browser_type.executable_path)
r"""
chromium C:\Users\ipetrash\AppData\Local\ms-playwright\chromium-1148\chrome-win\chrome.exe
firefox C:\Users\ipetrash\AppData\Local\ms-playwright\firefox-1466\firefox\firefox.exe
webkit C:\Users\ipetrash\AppData\Local\ms-playwright\webkit-2104\Playwright.exe
"""
