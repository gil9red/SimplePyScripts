#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install mechanize
import mechanize


br = mechanize.Browser()
br.open('https://docs.python.org/3/')

print(f'Title: {br.title()}')
print(f'URL: {br.geturl()}')
"""
Title: 3.11.1 Documentation
URL: https://docs.python.org/3/
"""

print()

br.follow_link(text_regex=r'Tutorial')

print(f'Title: {br.title()}')
print(f'URL: {br.geturl()}')
"""
Title: The Python Tutorial — Python 3.11.1 documentation
URL: https://docs.python.org/3/tutorial/index.html
"""
