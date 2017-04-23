#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def get_transitions_location(url_location):
    """
    Функция для поиска переходов из локации

    """

    import requests
    rs = requests.get(url_location)

    from bs4 import BeautifulSoup
    root = BeautifulSoup(rs.content, 'lxml')

    transitions = list()

    table_transitions = root.select_one('table.pi-horizontal-group')
    if not table_transitions or 'Переходы:' not in table_transitions.text:
        return transitions

    for a in table_transitions.select('a'):
        from urllib.parse import urljoin
        url = urljoin(rs.url, a['href'])

        transitions.append((url, a.text))

    return transitions


if __name__ == '__main__':
    url = 'http://ru.darksouls.wikia.com/wiki/Категория:Локации_(Dark_Souls_II)?display=page&sort=alphabetical'

    visited_locations = set()
    global_transitions = set()

    import requests
    rs = requests.get(url)

    from bs4 import BeautifulSoup
    root = BeautifulSoup(rs.content, 'lxml')

    for a in root.select('#mw-pages .mw-content-ltr a'):
        rel_url = a['href']

        from urllib.parse import urljoin
        url = urljoin(rs.url, rel_url)

        transitions = get_transitions_location(url)
        if not transitions:
            continue

        title = a.text.strip()
        print(title, url)

        title = title.lower()
        visited_locations.add(title)

        for url_trans, title_trans in transitions:
            title_trans = title_trans.lower().strip()

            print('    {} -> {}'.format(title_trans.title(), url_trans))

            # Проверяем что локации с обратной связью не занесены
            if (title_trans, title) not in global_transitions:
                global_transitions.add((title, title_trans))

        print('\n')

    visited_locations = [_.title() for _ in visited_locations]
    global_transitions = [(_.title(), __.title()) for _, __ in global_transitions]

    print(len(visited_locations), visited_locations)
    print(len(global_transitions), global_transitions)

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
