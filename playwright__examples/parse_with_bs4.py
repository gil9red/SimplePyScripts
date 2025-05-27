#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.firefox.launch()
    page = browser.new_page()

    rs = page.goto("https://httpbin.org/")
    text = rs.text()
    browser.close()

    soup = BeautifulSoup(text, "html.parser")
    print(soup.select_one("a.github-corner")["href"])
    print(soup.select_one(".description").get_text(strip=True, separator="\n"))
    """
    https://github.com/requests/httpbin
    A simple HTTP Request & Response Service.
    Run locally:
    $ docker run -p 80:80 kennethreitz/httpbin
    """
