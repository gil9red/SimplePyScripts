#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""Граф носителей гена Старшей Крови (ген Лары)"""


import os


COLOR_1 = "#8b00ff"
COLOR_2 = "blue"
COLOR_3 = "red"

GLOBAL_TRANSITIONS = {
    (("Лара Доррен", COLOR_1), ("Рианнон", COLOR_1)),
    (("Рианнон", COLOR_1), ("Фиона", COLOR_2)),
    (("Рианнон", COLOR_1), ("Амавет", COLOR_3)),
    (("Фиона", COLOR_2), ("Корбетт", COLOR_2)),
    (("Корбетт", COLOR_2), ("Дагорад", COLOR_2)),
    (("Адалия", COLOR_3), ("Калантэ", COLOR_1)),
    (("Дагорад", COLOR_2), ("Калантэ", COLOR_1)),
    (("Калантэ", COLOR_1), ("Паветта", COLOR_1)),
    (("Паветта", COLOR_1), ("Цири", COLOR_1)),
    (("Амавет", COLOR_3), ("Мюриель", COLOR_3)),
    (("Мюриель", COLOR_3), ("Адалия", COLOR_3)),
    (("Мюриель", COLOR_3), ("Роберт II", COLOR_3)),
}

edges = []
nodes = []

for _from, _to in GLOBAL_TRANSITIONS:
    if _from not in nodes:
        nodes.append(_from)

    if _to not in nodes:
        nodes.append(_to)

    edges.append({"source": nodes.index(_from), "target": nodes.index(_to)})

nodes_dict = [{"name": title, "color": color} for title, color in nodes]

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
