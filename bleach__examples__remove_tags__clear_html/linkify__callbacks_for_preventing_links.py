#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/mozilla/bleach
# SOURCE: https://bleach.readthedocs.io/en/latest/linkify.html#preventing-links


# pip install bleach
from bleach.linkifier import Linker


# Preventing Links

def dont_linkify_python(attrs, new=False):
    # This is an existing link, so leave it be
    if not new:
        return attrs
    # If the TLD is '.py', make sure it starts with http: or https:.
    # Use _text because that's the original text
    link_text = attrs['_text']
    if link_text.endswith('.py') and not link_text.startswith(('http:', 'https:')):
        # This looks like a Python file, not a URL. Don't make a link.
        return None
    # Everything checks out, keep going to the next callback.
    return attrs


linker = Linker(callbacks=[dont_linkify_python])
print(linker.linkify('abc http://example.com def'))
# abc <a href="http://example.com">http://example.com</a> def

print(linker.linkify('abc models.py def'))
# abc models.py def
