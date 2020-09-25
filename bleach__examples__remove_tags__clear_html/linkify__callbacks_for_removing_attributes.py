#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/mozilla/bleach
# SOURCE: https://bleach.readthedocs.io/en/latest/linkify.html#removing-attributes


# pip install bleach
from bleach.linkifier import Linker


# Removing Attributes

def allowed_attrs(attrs, new=False):
    """Only allow href, target, rel and title."""
    allowed = [
        (None, 'href'),
        (None, 'target'),
        (None, 'rel'),
        (None, 'title'),
        '_text',
    ]
    return dict((k, v) for k, v in attrs.items() if k in allowed)


linker = Linker(callbacks=[allowed_attrs])

html = '<a style="font-weight: super bold;" href="http://example.com">link</a>'
print(linker.linkify(html))
# <a href="http://example.com">link</a>

print()

def remove_title(attrs, new=False):
    attrs.pop((None, 'title'), None)
    return attrs

linker = Linker(callbacks=[remove_title])
print(linker.linkify('<a href="http://example.com">link</a>'))
# <a href="http://example.com">link</a>

print(linker.linkify('<a title="bad title" href="http://example.com">link</a>'))
# <a href="http://example.com">link</a>
