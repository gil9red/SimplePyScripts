#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://docs.python.org/3.6/library/pyexpat.html


import xml.parsers.expat


# 3 handler functions
def on_start_element(name, attrs):
    print("Start element:", name, attrs)


def on_end_element(name):
    print("End element:", name)


def on_char_data(data):
    print("Character data:", repr(data))


p = xml.parsers.expat.ParserCreate()
p.StartElementHandler = on_start_element
p.EndElementHandler = on_end_element
p.CharacterDataHandler = on_char_data

p.Parse(
    """\
<?xml version="1.0"?>
<parent id="top"><child1 name="paul">Text goes here</child1>
<child2 name="fred">More text</child2>
</parent>
""",
    1,
)
