#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install graphviz
from graphviz import Digraph


g = Digraph("G", filename="test-output/hello.gv")
g.edge("Hello", "World")
g.view()
