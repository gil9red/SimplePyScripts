#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/mozilla/bleach
# SOURCE: https://bleach.readthedocs.io/en/latest/linkify.html#using-bleach-linkifier-linkifyfilter


from functools import partial

# pip install bleach
from bleach import Cleaner
from bleach.linkifier import LinkifyFilter


html = '<pre>http://example.com</pre>'

cleaner = Cleaner(tags=['pre'])
print(cleaner.clean(html))
# <pre>http://example.com</pre>

cleaner = Cleaner(tags=['pre'], filters=[LinkifyFilter])
print(cleaner.clean(html))
# <pre><a href="http://example.com" rel="nofollow">http://example.com</a></pre>

print('\n' + '-' * 100 + '\n')

# skip_tags (list) – list of tags that you don’t want to linkify
# the contents of; for example, you could set this to ['pre']
# to skip linkifying contents of pre tags
cleaner = Cleaner(
    tags=['pre'],
    filters=[partial(LinkifyFilter, skip_tags=['pre'])]
)
print(cleaner.clean(html))
# <pre>http://example.com</pre>
