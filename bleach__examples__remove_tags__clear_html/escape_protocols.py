#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/mozilla/bleach
# SOURCE: https://bleach.readthedocs.io/en/latest/clean.html#allowed-protocols-protocols


# pip install bleach
import bleach


# List of allowed protocols
print('List of allowed protocols:', bleach.sanitizer.ALLOWED_PROTOCOLS)
# ['http', 'https', 'mailto']

print(
    bleach.clean(
        '<a href="smb://more_text">allowed protocol</a>'
    )
)
# <a>allowed protocol</a>

print(
    bleach.clean(
        '<a href="smb://more_text">allowed protocol</a>',
        protocols=['http', 'https', 'smb']
    )
)
# <a href="smb://more_text">allowed protocol</a>

print(
    bleach.clean(
        '<a href="smb://more_text">allowed protocol</a>',
        protocols=bleach.ALLOWED_PROTOCOLS + ['smb']
    )
)
# <a href="smb://more_text">allowed protocol</a>
