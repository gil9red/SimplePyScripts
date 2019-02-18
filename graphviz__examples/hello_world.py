#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# NOTE: HOW INSTALL:
#     Download and install: http://www.graphviz.org/download/
#     Append to PATH, example: C:\Program Files (x86)\Graphviz2.38\bin


# pip install graphviz
from graphviz import Digraph

dot = Digraph(comment='The Round Table')

dot.node('A', 'King Arthur')
dot.node('B', 'Sir Bedevere the Wise')
dot.node('L', 'Sir Lancelot the Brave')

dot.edges(['AB', 'AL'])
dot.edge('B', 'L', constraint='false')

dot.render('test-output/round-table.gv', view=True)
