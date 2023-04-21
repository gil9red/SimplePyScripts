#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/mozilla/bleach
# SOURCE: https://bleach.readthedocs.io/en/latest/clean.html#html5lib-filters-filters


# pip install bleach
from bleach.sanitizer import Cleaner
from bleach.html5lib_shim import Filter


class MooFilter(Filter):
    def __iter__(self):
        for token in super().__iter__():
            if token["type"] in ["StartTag", "EmptyTag"] and token["data"]:
                for attr, value in token["data"].items():
                    token["data"][attr] = "moo"
            yield token


TAGS = ["img"]
ATTRS = {
    "img": ["rel", "src"],
}

html = 'this is cute! <img src="http://example.com/puppy.jpg" rel="nofollow">'

cleaner = Cleaner(tags=TAGS, attributes=ATTRS, filters=[MooFilter])
print(cleaner.clean(html))
# this is cute! <img rel="moo" src="moo">
