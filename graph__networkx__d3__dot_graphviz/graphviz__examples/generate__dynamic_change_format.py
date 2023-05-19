#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install graphviz
from graphviz import Digraph


g = Digraph("G", format="svg")
g.edge("Hello", "World")

# Get bytes
print(g.pipe())

g.format = "png"
print(g.pipe())

g.format = "pdf"
print(g.pipe())
