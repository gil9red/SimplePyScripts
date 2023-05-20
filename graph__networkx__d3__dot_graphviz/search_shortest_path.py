#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# TODO: пример работы с networkx
# http://networkx.github.io/
# http://networkx.github.io/documentation/latest/gallery.html
# http://networkx.github.io/documentation/latest/reference/index.html
# http://habrahabr.ru/post/125898/
# http://habrahabr.ru/post/129344/


import networkx as nx


g = nx.Graph()
g.add_edge("A", "B", weight=4)
g.add_edge("B", "D", weight=2)
g.add_edge("A", "C", weight=3)
g.add_edge("C", "D", weight=4)

print(nx.shortest_path(g, "A", "D", weight="weight"))
