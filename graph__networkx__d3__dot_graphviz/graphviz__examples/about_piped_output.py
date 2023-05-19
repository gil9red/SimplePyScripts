#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://graphviz.readthedocs.io/en/stable/manual.html#piped-output


# pip install graphviz
from graphviz import Digraph


g = Digraph("hello", format="svg")
g.edge("Hello", "World")
print(g.pipe().decode("utf-8"))
# <?xml version="1.0" encoding="UTF-8" standalone="no"?>
# <!DOCTYPE svg
# ...
# </svg>
