#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    for browser_type in [p.chromium, p.firefox, p.webkit]:
        browser = browser_type.launch()
        page = browser.new_page()

        print(browser_type.name.upper())
        print("Local:", page.evaluate("navigator.userAgent"))

        context = browser.new_context(user_agent="Abc 123")
        print("Set local:", context.new_page().evaluate("navigator.userAgent"))

        rs = page.goto("https://httpbin.org/user-agent")
        print("Remote:", rs.json()["user-agent"])

        print()

        browser.close()
"""
CHROMIUM
Local: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/131.0.6778.33 Safari/537.36
Set local: Abc 123
Remote: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/131.0.6778.33 Safari/537.36

FIREFOX
Local: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0
Set local: Abc 123
Remote: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0

WEBKIT
Local: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Safari/605.1.15
Set local: Abc 123
Remote: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Safari/605.1.15
"""
