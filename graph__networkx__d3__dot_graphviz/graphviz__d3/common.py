#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
sys.path.append("../graphviz__examples/ds2_locations")


# SOURCE: https://github.com/magjac/d3-graphviz
with open("template.html", encoding="utf-8") as f:
    TEMPLATE = f.read()


def generate(graph) -> str:
    return TEMPLATE.format(dot_src=str(graph))
