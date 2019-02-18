#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install graphviz
from graphviz import Digraph

g = Digraph(comment='The Round Table')
g.edge('Hello', 'World')

out_file_name = g.render('test-output/hello_world.gv')
print(out_file_name)
