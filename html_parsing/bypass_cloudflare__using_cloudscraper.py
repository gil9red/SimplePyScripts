#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import cloudscraper
import requests


url = "https://tofunft.com/ru/collection/iguverse-nft/activities?category=listing"


scraper = cloudscraper.create_scraper()
rs = scraper.get(url)
print(rs)
print(rs.content[:100])
"""
<Response [200]>
b'<!DOCTYPE html><html translate="no" lang="ru"><head><link rel="preconnect" href="https://fonts.googl'
"""

print()

rs = requests.get(url)
print(rs)
print(rs.content[:100])
"""
<Response [403]>
b'<!DOCTYPE html>\n<html lang="en-US">\n<head>\n    <title>Just a moment...</title>\n    <meta http-equiv='
"""
