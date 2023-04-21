#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/mozilla/bleach
# SOURCE: https://bleach.readthedocs.io/en/latest/clean.html#allowed-attributes-attributes


from urllib.parse import urlparse

# pip install bleach
import bleach


# Map of allowed attributes by tag:
print("Map of allowed attributes by tag:", bleach.sanitizer.ALLOWED_ATTRIBUTES)
# {'a': ['href', 'title'], 'abbr': ['title'], 'acronym': ['title']}

# As a list
print(
    bleach.clean(
        '<p class="foo" style="color: red; font-weight: bold;">blah blah blah</p>',
        tags=["p"],
        attributes=["style"],
        styles=["color"],
    )
)
# <p style="color: red;">blah blah blah</p>

# As a dict
attrs = {
    "*": ["class"],  # Any tag with class
    "a": ["href", "rel"],
    "img": ["alt"],
}
print(
    bleach.clean(
        '<img alt="an example" width=500>',
        tags=["img"],
        attributes=attrs,
    )
)
# <img alt="an example">

print()


#
# Using functions
#
def allow_h(tag, name, value):
    return name[0] == "h"


print(
    bleach.clean(
        '<a href="http://example.com" title="link">link</a>',
        tags=["a"],
        attributes=allow_h,
    )
)
# <a href="http://example.com">link</a>


def allow_src(tag, name, value):
    if name in ("alt", "height", "width"):
        return True
    if name == "src":
        p = urlparse(value)
        return not p.netloc or p.netloc == "mydomain.com"
    return False


print(
    bleach.clean(
        '<img src="http://example.com" alt="an example">',
        tags=["img"],
        attributes={
            "img": allow_src
        },
    )
)
# <img alt="an example">
