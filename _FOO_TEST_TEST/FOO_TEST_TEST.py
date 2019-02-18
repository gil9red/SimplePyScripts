#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'




quit()


# TODO: добавить пример графа из ds1 отрисованного через graphviz

# TODO: добавить пример получения из графа текст на DOT (https://ru.wikipedia.org/wiki/DOT_(%D1%8F%D0%B7%D1%8B%D0%BA))

# # pip install graphviz
# from graphviz import Digraph
#
# t = Digraph('TrafficLights', filename='traffic_lights.gv', engine='neato')
#
# t.attr('node', shape='box')
# for i in (2, 1):
#     t.node('gy%d' % i)
#     t.node('yr%d' % i)
#     t.node('rg%d' % i)
#
# t.attr('node', shape='circle', fixedsize='true', width='0.9')
# for i in (2, 1):
#     t.node('green%d' % i)
#     t.node('yellow%d' % i)
#     t.node('red%d' % i)
#     t.node('safe%d' % i)
#
# for i, j in [(2, 1), (1, 2)]:
#     t.edge('gy%d' % i, 'yellow%d' % i)
#     t.edge('rg%d' % i, 'green%d' % i)
#     t.edge('yr%d' % i, 'safe%d' % j)
#     t.edge('yr%d' % i, 'red%d' % i)
#     t.edge('safe%d' % i, 'rg%d' % i)
#     t.edge('green%d' % i, 'gy%d' % i)
#     t.edge('yellow%d' % i, 'yr%d' % i)
#     t.edge('red%d' % i, 'rg%d' % i)
#
# t.attr(overlap='false')
# t.attr(label=r'PetriNet Model TrafficLights\n'
#              r'Extracted from ConceptBase and layed out by Graphviz')
# t.attr(fontsize='12')
#
# t.view()

# from graphviz import Graph
# g = Graph('G', filename='process.gv', engine='sfdp')
#
# g.edge('run', 'intr')
# g.edge('intr', 'runbl')
# g.edge('runbl', 'run')
# g.edge('run', 'kernel')
# g.edge('kernel', 'zombie')
# g.edge('kernel', 'sleep')
# g.edge('kernel', 'runmem')
# g.edge('sleep', 'swap')
# g.edge('swap', 'runswap')
# g.edge('runswap', 'new')
# g.edge('runswap', 'runmem')
# g.edge('new', 'runmem')
# g.edge('sleep', 'runmem')
#
# g.view()

# TODO: сравнить чем отличаются engine: dot, neato, ...
# C:\ProgramData\Anaconda3\Lib\site-packages\graphviz\backend.py
# ENGINES = {  # http://www.graphviz.org/pdf/dot.1.pdf
#     'dot', 'neato', 'twopi', 'circo', 'fdp', 'sfdp', 'patchwork', 'osage',
# }
# TODO: http://www.graphviz.org/pdf/dot.1.pdf
# import graphviz
# print(graphviz.ENGINES)


# TODO: поискать какие форматы еще поддерживаются:
#       https://graphviz.gitlab.io/doc/info/output.html
#       https://graphviz.readthedocs.io/en/stable/manual.html#formats
#   C:\ProgramData\Anaconda3\Lib\site-packages\graphviz\backend.py
#     FORMATS = {  # http://www.graphviz.org/doc/info/output.html
#         'bmp',
#         'canon', 'dot', 'gv', 'xdot', 'xdot1.2', 'xdot1.4',
#         'cgimage',
