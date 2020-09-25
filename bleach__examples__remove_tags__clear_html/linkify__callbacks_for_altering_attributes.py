#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/mozilla/bleach
# SOURCE: https://bleach.readthedocs.io/en/latest/linkify.html#altering-attributes


from urllib.parse import urlparse, quote

# pip install bleach
from bleach.linkifier import Linker


# Altering Attributes

def shorten_url(attrs, new=False):
    """Shorten overly-long URLs in the text."""
    # Only adjust newly-created links
    if not new:
        return attrs
    # _text will be the same as the URL for new links
    text = attrs['_text']
    if len(text) > 25:
        attrs['_text'] = text[:22] + '...'
    return attrs

linker = Linker(callbacks=[shorten_url])
print(linker.linkify('http://example.com/longlonglonglonglongurl'))
# <a href="http://example.com/longlonglonglonglongurl">http://example.com/lon...</a>

print(linker.linkify('abc <a href="http://example.com/longlonglonglonglongurl">http://example.com/longlonglonglonglongurl</a> def'))
# abc <a href="http://example.com/longlonglonglonglongurl">http://example.com/longlonglonglonglongurl</a> def

print()

def outgoing_bouncer(attrs, new=False):
    """Send outgoing links through a bouncer."""
    href_key = (None, 'href')
    p = urlparse(attrs.get(href_key))
    if p.netloc not in ['example.com', 'www.example.com', '']:
        url = attrs[href_key]
        bouncer = 'http://bn.ce/?destination=%s'
        attrs[href_key] = bouncer % quote(url)
    return attrs

linker = Linker(callbacks=[outgoing_bouncer])
print(linker.linkify('http://example.com'))
# <a href="http://example.com">http://example.com</a>

print(linker.linkify('http://foo.com'))
# <a href="http://bn.ce/?destination=http%3A//foo.com">http://foo.com</a>
