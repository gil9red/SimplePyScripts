#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/mozilla/bleach
# SOURCE: https://bleach.readthedocs.io/en/latest/linkify.html#bleach.linkify


# pip install bleach
import bleach


html = '''
http://example.com
hello_world@example.com
'''.strip()
print(bleach.linkify(html, parse_email=True))
# <a href="http://example.com" rel="nofollow">http://example.com</a>
# <a href="mailto:hello_world@example.com">hello_world@example.com</a>
