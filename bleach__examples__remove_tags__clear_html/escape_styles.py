#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/mozilla/bleach
# SOURCE: https://bleach.readthedocs.io/en/latest/clean.html#allowed-styles-styles


# pip install bleach
import bleach


# List of allowed styles
print('List of allowed styles:', bleach.sanitizer.ALLOWED_STYLES)
# []

tags = ['p', 'em', 'strong']
attrs = {
    # Any tag with style
    '*': ['style']
}
styles = ['color', 'font-weight']

html = '<p style="font-weight: heavy; font-family: Arial; background-color: brown;">my html</p>'
print(
    bleach.clean(
        html,
        tags=tags,
        attributes=attrs,
        styles=styles
    )
)
# <p style="font-weight: heavy;">my html</p>
