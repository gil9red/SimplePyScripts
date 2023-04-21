#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/mozilla/bleach
# SOURCE: https://bleach.readthedocs.io/en/latest/linkify.html#removing-links


# pip install bleach
from bleach.linkifier import Linker


# Removing Links


def remove_mailto(attrs, new=False):
    if attrs[(None, "href")].startswith("mailto:"):
        return None
    return attrs


linker = Linker(callbacks=[remove_mailto])


html = """
<a href="mailto:janet@example.com">mail janet!</a>
abc <a href="http://example.com">http://example.com</a> def
""".strip()
print(linker.linkify(html))
# mail janet!
# abc <a href="http://example.com">http://example.com</a> def
