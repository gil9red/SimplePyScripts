#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/mozilla/bleach
# SOURCE: https://bleach.readthedocs.io/en/latest/clean.html#using-bleach-sanitizer-cleaner


# pip install bleach
from bleach.sanitizer import Cleaner


html = """
<p><span>is not <b><span>allowed</span></b></span></p>
<p><b>Hello World!</b></p>
""".strip()

cleaner = Cleaner()

for text in html.splitlines():
    print(cleaner.clean(text))
# &lt;p&gt;&lt;span&gt;is not <b>&lt;span&gt;allowed&lt;/span&gt;</b>&lt;/span&gt;&lt;/p&gt;
# &lt;p&gt;<b>Hello World!</b>&lt;/p&gt;

print()

cleaner = Cleaner(tags=["b", "span"], strip=True)
for text in html.splitlines():
    print(cleaner.clean(text))
# <span>is not <b><span>allowed</span></b></span>
# <b>Hello World!</b>
