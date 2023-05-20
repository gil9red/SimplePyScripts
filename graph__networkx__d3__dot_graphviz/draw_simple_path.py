#!/usr/bin/env python

# SOURCE: https://networkx.readthedocs.io/en/stable/examples/drawing/simple_path.html

"""
Draw a graph with matplotlib.
You must have matplotlib for this to work.

"""

import networkx as nx
import matplotlib.pyplot as plt


g = nx.path_graph(8)
nx.draw(g)

plt.savefig("simple_path.png")  # save as png
plt.show()  # display
