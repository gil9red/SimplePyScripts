#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install graphviz
from graphviz import Digraph


g = Digraph("G", filename="hello", format="png")
g.edge("Hello", "World")

# Save
with open(g.filepath + "." + g.format, "wb") as f:
    data = g.pipe()
    f.write(data)
