#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import networkx as nx
import matplotlib.pyplot as plt

from Dark_Souls_II__print_locations_from_start_location import print_transitions


links = set()
visited_locations = set()
url_start_location = "http://ru.darksouls.wikia.com/wiki/Междумирье"

print_transitions(url_start_location, "Междумирье", visited_locations, links, log=False)

print()
print(len(visited_locations), sorted(visited_locations))
print(len(links), sorted(links))

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

# plt.figure(1)
plt.axis("off")
# plt.savefig("ds2_locations_graph.png")  # save as png
plt.show()  # display
