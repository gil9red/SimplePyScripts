#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install graphviz
from graphviz import Digraph


g = Digraph("G", filename="test-output/hello_world.gv")
g.edge("Hello", "World")

# Delete the source file after rendering.
out_file_name = g.render(cleanup=True)
print(out_file_name)
