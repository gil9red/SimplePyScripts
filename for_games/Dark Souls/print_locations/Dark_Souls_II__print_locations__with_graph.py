#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
sys.path.append("..")

import networkx as nx
import matplotlib.pyplot as plt

from common import find_links_ds2


links = find_links_ds2()
print(len(links), links)

# Составим граф локаций
# TODO: pretty graph

G = nx.Graph()

for source, target in links:
    G.add_edge(source, target)

pos = nx.spring_layout(G)  # positions for all nodes

# edges
nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=6)

# nodes
nx.draw_networkx_nodes(G, pos, node_size=70)

# labels
nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")

plt.axis("off")
# plt.savefig("ds2_locations_graph.png")  # save as png
plt.show()  # display
