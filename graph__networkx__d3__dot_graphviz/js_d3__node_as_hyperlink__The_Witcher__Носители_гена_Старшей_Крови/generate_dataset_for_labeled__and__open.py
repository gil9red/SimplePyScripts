#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""Граф носителей гена Старшей Крови (ген Лары)"""


import os


COLOR_1 = "#8b00ff"
COLOR_2 = "blue"
COLOR_3 = "red"

# TODO: ?
# TREE = {
#     'name': 'Лара Доррен', 'color': COLOR_1,
#     'href': 'http://vedmak.wikia.com/wiki/Лара_Доррен_аэп_Шиадаль',
#     'children': [
#         {
#             'name': 'Рианнон', 'color': COLOR_1, 'href': 'http://vedmak.wikia.com/wiki/Рианнон',
#             'children': [
#             # ...
#             ],
#         }
#     ],
# }

NODE_1 = (
    "Лара Доррен",
    COLOR_1,
    "http://vedmak.wikia.com/wiki/Лара_Доррен_аэп_Шиадаль",
)
NODE_2 = ("Рианнон", COLOR_1, "http://vedmak.wikia.com/wiki/Рианнон")
NODE_3 = ("Фиона", COLOR_2, "http://vedmak.wikia.com/wiki/Фиона")
NODE_4 = ("Амавет", COLOR_3, "http://vedmak.wikia.com/wiki/Амавет")
NODE_5 = ("Корбетт", COLOR_2, "http://vedmak.wikia.com/wiki/Корбетт")
NODE_6 = ("Дагорад", COLOR_2, "http://vedmak.wikia.com/wiki/Дагорад")
NODE_7 = ("Адалия", COLOR_3, "http://vedmak.wikia.com/wiki/Адалия")
NODE_8 = ("Мюриель", COLOR_3, "http://vedmak.wikia.com/wiki/Мюриель")
NODE_9 = ("Роберт II", COLOR_3, "http://vedmak.wikia.com/wiki/Роберт II")
NODE_10 = ("Калантэ", COLOR_1, "http://vedmak.wikia.com/wiki/Калантэ")
NODE_11 = ("Паветта", COLOR_1, "http://vedmak.wikia.com/wiki/Паветта")
NODE_12 = ("Цири", COLOR_1, "http://vedmak.wikia.com/wiki/Цири")


GLOBAL_TRANSITIONS = {
    (NODE_1, NODE_2),
    (NODE_2, NODE_3),
    (NODE_2, NODE_4),
    (NODE_3, NODE_5),
    (NODE_5, NODE_6),
    (NODE_7, NODE_10),
    (NODE_6, NODE_10),
    (NODE_10, NODE_11),
    (NODE_11, NODE_12),
    (NODE_4, NODE_8),
    (NODE_8, NODE_7),
    (NODE_8, NODE_9),
}

edges = list()
nodes = list()

for _from, _to in GLOBAL_TRANSITIONS:
    if _from not in nodes:
        nodes.append(_from)

    if _to not in nodes:
        nodes.append(_to)

    edges.append({"source": nodes.index(_from), "target": nodes.index(_to)})

nodes_dict = [
    {"name": title, "color": color, "href": href} for title, color, href in nodes
]

dataset_text = f"""\
    var dataset = {{
        nodes: {nodes_dict},
        edges: {edges}
    }};
"""
print(dataset_text)

with open("template__graph_with_labeled_edges.html", "r", encoding="utf-8") as f:
    text = f.read()
    text = text.replace("{{dataset}}", dataset_text)

with open("graph_with_labeled_edges.html", "w", encoding="utf-8") as f:
    f.write(text)

# Open file
os.startfile("graph_with_labeled_edges.html")
