#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/mozilla/bleach
# SOURCE: https://bleach.readthedocs.io/en/latest/clean.html#allowed-tags-tags


# pip install bleach
import bleach


# List of allowed tags
print('List of allowed tags:', bleach.sanitizer.ALLOWED_TAGS)
# ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'strong', 'ul']

print(bleach.clean('an <script>evil()</script> example'))
# an &lt;script&gt;evil()&lt;/script&gt; example

# Allowed tags
print(
    bleach.clean(
        '<b><i>an example</i></b>',
        tags=['b'],
    )
)
# <b>&lt;i&gt;an example&lt;/i&gt;</b>
