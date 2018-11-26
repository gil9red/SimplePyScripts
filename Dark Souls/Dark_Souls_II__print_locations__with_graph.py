#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from Dark_Souls_II__print_locations import find_locations


visited_locations, global_transitions = find_locations()

print(len(visited_locations), sorted(visited_locations))
print(len(global_transitions), sorted(global_transitions))

# Составим граф локаций
# TODO: pretty graph
import networkx as nx
G = nx.Graph()

for title, title_trans in global_transitions:
    G.add_edge(title, title_trans)

pos = nx.spring_layout(G)  # positions for all nodes

# edges
nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=6)

# nodes
nx.draw_networkx_nodes(G, pos, node_size=70)

# labels
nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')

import matplotlib.pyplot as plt
plt.axis('off')
# plt.savefig("ds2_locations_graph.png")  # save as png
plt.show()  # display
