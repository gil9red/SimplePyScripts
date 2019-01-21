#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from collections import defaultdict
from glob import iglob
import os


def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)

        num /= 1024.0

    return "%3.1f %s" % (num, 'TB')


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/b6ac435ee171e48ed35044e8e61e199de641a6e7/get_dir_total_size__using_glob.py
def get_dir_total_size(dir_name: str) -> (int, str):
    total_size = 0

    for file_name in iglob(dir_name + '/**/*', recursive=True):
        try:
            if os.path.isfile(file_name):
                total_size += os.path.getsize(file_name)

        except Exception as e:
            print('File: "{}", error: "{}"'.format(file_name, e))

    return total_size, sizeof_fmt(total_size)


paths = [
    'C:\\Program Files (x86)\\Raft',
    'C:\\Program Files (x86)\\Spirits of Mystery 11. The Lost Queen CE',
    'C:\\Wowangames\\Saga of the Nine Worlds 3. The Hunt CE RUS',
    'C:\\Wowangames\\Saga of the Nine Worlds. The Gathering CE RUS',
    'C:\\Wowangames\\Saga Of The Nine Worlds 2. The Four Stags CE RUS',
    "D:\\Program Files (x86)\\R.G. Mechanics\\Alan Wake's American Nightmare",
    'D:\\Program Files (x86)\\R.G. Mechanics\\Alan Wake',
    'D:\\Games\\Borderlands',
    'D:\\Program Files (x86)\\R.G. Mechanics\\Dark Souls - Prepare to Die Edition',
    'D:\\Games\\Dark Souls II Scholar of the First Sin',
    'D:\\R.G. Catalyst\\DARK SOULS REMASTERED',
    'D:\\Games\\FFXV',
    'D:\\Program Files (x86)\\Final Fantasy XV',
    'D:\\Games\\Ghost of a Tale',
    'D:\\Games\\Life Goes On - Done to Death',
    'D:\\Program Files (x86)\\Masters of Anima',
    'D:\\Games\\One Piece - Burning Blood',
    'D:\\Program Files (x86)\\Resident Evil HD Remaster',
    'D:\\Games\\ROTTR - 20 Year Celebration',
    'D:\\R.G. Catalyst\\Saints Row - Gat Out of Hell',
    'D:\\Program Files (x86)\\R.G. Mechanics\\Sniper Elite',
    'D:\\Program Files (x86)\\Steel Rats',
    'D:\\Games\\Tales of Berseria',
    'D:\\Games\\The Evil Within 2',
    'D:\\Games\\The Evil Within',
    'D:\\Program Files (x86)\\R.G. Mechanics\\Tomb Raider',
    'D:\\Program Files (x86)\\Willy-Nilly Knight',
    'E:\\Program Files (x86)\\Ashes',
    'E:\\Games\\Grow Up',
    'E:\\Program Files (x86)\\Rezrog',
    'E:\\Games\\Tekken 7'
]

total_size = 0
total_size_by_disc = defaultdict(int)

for file_name in paths:
    size, size_str = get_dir_total_size(file_name)
    print('{:<15} {:10} {}'.format(size, size_str, file_name))

    total_size += size
    total_size_by_disc[file_name[0]] += size

print('\n')

print(total_size, sizeof_fmt(total_size))

for disc, size in sorted(total_size_by_disc.items(), key=lambda x: x[0]):
    print(disc, size, sizeof_fmt(size))


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

