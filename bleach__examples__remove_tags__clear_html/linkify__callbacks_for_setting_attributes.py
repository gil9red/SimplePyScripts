#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/mozilla/bleach
# SOURCE: https://bleach.readthedocs.io/en/latest/linkify.html#callbacks-for-adjusting-attributes-callbacks


from urllib.parse import urlparse

# pip install bleach
from bleach.linkifier import Linker


# Setting Attributes

def set_title(attrs, new=False):
    attrs[(None, 'title')] = 'link in user text'
    return attrs

linker = Linker(callbacks=[set_title])
print(linker.linkify('abc http://example.com def'))
# abc <a href="http://example.com" title="link in user text">http://example.com</a> def

print()

def set_target(attrs, new=False):
    p = urlparse(attrs[(None, 'href')])
    if p.netloc not in ['my-domain.com', 'other-domain.com']:
        attrs[(None, 'target')] = '_blank'
        attrs[(None, 'class')] = 'external'
    else:
        attrs.pop((None, 'target'), None)
    return attrs

html = '''
abc http://example.com def
123 https://my-domain.com 456
!!! <a class="local" href="https://my-domain.com" target="_blank">https://my-domain.com</a> ###
'''.strip()
linker = Linker(callbacks=[set_target])
print(linker.linkify(html))
# abc <a class="external" href="http://example.com" target="_blank">http://example.com</a> def
# 123 <a href="https://my-domain.com">https://my-domain.com</a> 456
# !!! <a class="local" href="https://my-domain.com">https://my-domain.com</a> ###
