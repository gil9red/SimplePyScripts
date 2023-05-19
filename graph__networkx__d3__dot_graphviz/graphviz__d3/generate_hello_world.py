#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from common import generate

# pip install graphviz
from graphviz import Digraph


def get_graph():
    g = Digraph("G")
    g.edge("Hello", "World")
    return g


FILE_NAME = "hello_world.html"


if __name__ == "__main__":
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        g = get_graph()
        text = generate(g)
        f.write(text)
