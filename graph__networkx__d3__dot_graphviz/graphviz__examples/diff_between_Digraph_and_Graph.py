#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install graphviz
from graphviz import Digraph, Graph


# Directed graph
g = Digraph("G", filename="test-output/hello_Digraph.gv")
g.edge("Hello", "World")
g.view(cleanup=True)

g = Graph("G", filename="test-output/hello_Graph.gv")
g.edge("Hello", "World")
g.view(cleanup=True)
