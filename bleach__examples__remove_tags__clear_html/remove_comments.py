#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/mozilla/bleach
# SOURCE: https://bleach.readthedocs.io/en/latest/clean.html#stripping-comments-strip-comments


# pip install bleach
import bleach


html = "my<!-- commented --> html"

print(bleach.clean(html))
# my html

print(bleach.clean(html, strip_comments=False))
# my<!-- commented --> html
