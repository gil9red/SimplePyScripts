#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.webkit.launch()
    page = browser.new_page()

    rs = page.goto("https://httpbin.org/")
    print(rs.text())

    browser.close()
