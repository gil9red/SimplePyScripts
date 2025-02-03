#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    for browser_type in [p.chromium, p.firefox, p.webkit]:
        browser = browser_type.launch()
        page = browser.new_page()

        print(browser_type.name.upper())

        print("Cookies:", page.context.cookies())

        for k, v in [
            ("name", 123),
            ("foo", "bar"),
            ("browser", browser_type.name),
        ]:
            page.goto(f"https://httpbin.org/cookies/set/{k}/{v}")
            time.sleep(1)

        rs = page.goto("https://httpbin.org/cookies")
        print("From API:", rs.json())

        cookies = page.context.cookies()
        print(f"Cookies ({len(cookies)}):")
        for cookie in cookies:
            print(f"    {cookie}")

        print()

    browser.close()
"""
CHROMIUM
Cookies: []
From API: {'cookies': {'browser': 'chromium', 'foo': 'bar', 'name': '123'}}
Cookies (3):
    {'name': 'name', 'value': '123', 'domain': 'httpbin.org', 'path': '/', 'expires': -1, 'httpOnly': False, 'secure': False, 'sameSite': 'Lax'}
    {'name': 'foo', 'value': 'bar', 'domain': 'httpbin.org', 'path': '/', 'expires': -1, 'httpOnly': False, 'secure': False, 'sameSite': 'Lax'}
    {'name': 'browser', 'value': 'chromium', 'domain': 'httpbin.org', 'path': '/', 'expires': -1, 'httpOnly': False, 'secure': False, 'sameSite': 'Lax'}

FIREFOX
Cookies: []
From API: {'cookies': {'browser': 'firefox', 'foo': 'bar', 'name': '123'}}
Cookies (3):
    {'name': 'name', 'value': '123', 'domain': 'httpbin.org', 'path': '/', 'expires': -1, 'httpOnly': False, 'secure': False, 'sameSite': 'None'}
    {'name': 'foo', 'value': 'bar', 'domain': 'httpbin.org', 'path': '/', 'expires': -1, 'httpOnly': False, 'secure': False, 'sameSite': 'None'}
    {'name': 'browser', 'value': 'firefox', 'domain': 'httpbin.org', 'path': '/', 'expires': -1, 'httpOnly': False, 'secure': False, 'sameSite': 'None'}

WEBKIT
Cookies: []
From API: {'cookies': {}}
Cookies (0):

"""
