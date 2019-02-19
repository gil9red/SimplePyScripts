#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# NOTE: HOW INSTALL:
#     Download and install: http://www.graphviz.org/download/
#     Append to PATH, example: C:\Program Files (x86)\Graphviz2.38\bin


# pip install graphviz
from graphviz import Digraph

g = Digraph(comment='The Round Table')

g.node('A', 'King Arthur')
g.node('B', 'Sir Bedevere the Wise')
g.node('L', 'Sir Lancelot the Brave')

g.edges(['AB', 'AL'])
g.edge('B', 'L', constraint='false')

g.render('test-output/round-table.gv', view=True)
