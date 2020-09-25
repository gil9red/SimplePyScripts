#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/mozilla/bleach
# SOURCE: https://bleach.readthedocs.io/en/latest/clean.html#stripping-markup-strip


# pip install bleach
import bleach


html = '<p><span>is not <b><span>allowed</span></b></span></p>'

print(bleach.clean(html))
# &lt;p&gt;&lt;span&gt;is not <b>&lt;span&gt;allowed&lt;/span&gt;</b>&lt;/span&gt;&lt;/p&gt;

# About <b> see here bleach.sanitizer.ALLOWED_TAGS
print(bleach.clean(html, strip=True))
# is not <b>allowed</b>

print(bleach.clean(html, tags=[], strip=True))
# is not allowed
