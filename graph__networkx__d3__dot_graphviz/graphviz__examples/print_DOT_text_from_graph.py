#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install graphviz
from graphviz import Digraph


g = Digraph(comment="The Round Table")

g.node("A", "King Arthur")
g.node("B", "Sir Bedevere the Wise")
g.node("L", "Sir Lancelot the Brave")

g.edges(["AB", "AL"])
g.edge("B", "L", constraint="false")
# g.view()

dot_text = str(g)
print(dot_text)
