#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'




quit()

# TODO: инструкцию поместить в будущий hello_world.py
# Download and install: http://www.graphviz.org/download/
# Append to PATH: C:\Program Files (x86)\Graphviz2.38\bin

# pip install graphviz
from graphviz import Digraph

# dot = Digraph(comment='The Round Table')
#
# dot.node('A', 'King Arthur')
# dot.node('B', 'Sir Bedevere the Wise')
# dot.node('L', 'Sir Lancelot the Brave')
#
# dot.edges(['AB', 'AL'])
# dot.edge('B', 'L', constraint='false')
#
# dot.render('test-output/round-table.gv', view=True)



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

# TODO: на примере показать разницу между Digraph (граф с направлением) и Graph

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


# from graphviz import Digraph
# g = Digraph('G', filename='hello.gv')
# g.edge('Hello', 'World')
# g.view()


# TODO: пример чистой генерации без показа
# from graphviz import Digraph
# g = Digraph('G', filename='hello.gv', format='png')
# g.edge('Hello', 'World')
# # g.view()
# g.render()


# TODO: нужен прпимер в котором сгенерированный *.gv файл будет удален
from graphviz import Digraph
# g = Digraph('G', filename='hello.gv', format='png')
g = Digraph('G', filename='hello.gv', format='pdf')
g.edge('Hello', 'World')

# Delete the source file after rendering.
g.render(cleanup=True)


# TODO: еще один пример генерации, в отличии от верхнего, *.gv файл не был создан
#       и, соответственно, не пришлось его удалять
#       Более надежно, чем выше
from graphviz import Digraph
g = Digraph('G', filename='hello.gv', format='png')
# TODO: добавить пример динамической смены формата
g.format = 'plain'
g.edge('Hello', 'World')
# print(g)
# Save
with open(g.filepath + '.' + g.format, 'wb') as f:
    data = g.pipe()
    # print(data)
    f.write(data)


# TODO: добавить прмиер получения результат генерации в байтах,
#       в строке (для определенного формата, например для 'plain' или 'svg')
# from graphviz import Digraph
# # g = Digraph('G', filename='hello.gv', format='png')
# g = Digraph('G', filename='hello.gv', format='pdf')
# g.edge('Hello', 'World')
# # Get bytes
# print(g.pipe())
#
# TODO: Piped output
# https://graphviz.readthedocs.io/en/stable/manual.html#piped-output
# >>> g = Graph('hello', format='svg')
#
# >>> g.edge('Hello', 'World')
#
# >>> print(g.pipe().decode('utf-8'))
# <?xml version="1.0" encoding="UTF-8" standalone="no"?>
# <!DOCTYPE svg
# ...
# </svg>


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
#
# import graphviz
# print(graphviz.FORMATS)

# from graphviz import Digraph
# g = Digraph('G', filename='hello.gv', format='svg')
# g.edge('Hello', 'World')
# # g.view()
# g.render()


# TODO: версия
# import graphviz
# print(graphviz.version())

