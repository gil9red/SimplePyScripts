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
    # NOTE: Способ поиска локаций, начиная с начальной и через переходы локаций искать другие сработал, однако
    # одна локация потерялась -- "Темная Бездна Былого", локация, что была с ней связана не указывала на
    # эту локацию в переходах

    global_transitions = set()

    # NOTE: For test rendering graph
    CACHE = True
    if CACHE:
        global_transitions = {('Маджула', 'Лес Павших Гигантов'), ('Лес Павших Гигантов', 'Память Ваммара'), ('Мглистая Башня', 'Память старого железного короля'), ('Замок Дранглик', 'Трон Желания'), ('Междумирье', 'Маджула'), ('Могила Святых', 'Помойка'), ('Маджула', 'Помойка'), ('Ледяная Элеум Лойс', 'Холодные Окраины'), ('Храм Зимы', ' Ледяная Элеум Лойс'), ('Гнездо Дракона', 'Храм Дракона'), ('Темнолесье', 'Двери Фарроса'), ('Маджула', 'Темнолесье'), ('Железная Цитадель', 'Земляной Пик'), ('Лес Павших Гигантов', 'Память Орро'), ('Королевский проход', 'Храм Аманы'), ('Темнолесье', 'Цитадель Алдии'), ('Роща Охотника', 'Долина Жатвы'), ('Маджула', 'Могила Святых'), ('Шульва, Священный город', 'Святилище дракона'), ('Храм Аманы', 'Королевский проход '), (' Ледяная Элеум Лойс', 'Большой собор'), ('Склеп Нежити', 'Память Короля'), ('Королевский проход ', 'Замок Дранглик'), ('Земляной Пик', 'Железная цитадель'), ('Бухта Брайтстоун-Тселдора', 'Воспоминания Дракона'), (' Ледяная Элеум Лойс', 'Холодные Окраины'), ('Храм Аманы', 'Склеп Нежити'), ('Черная Расселина', 'Шульва, Священный город'), ('Огненная Башня Хейда', 'Маджула'), ('Храм Зимы', 'Замок Дранглик'), ('Огненная Башня Хейда', 'Собор Лазурного Пути'), ('Лес Павших Гигантов', 'Память Джейта'), ('Двери Фарроса', 'Бухта Брайтстоун-Тселдора'), ('Цитадель Алдии', 'Гнездо Дракона'), ('Роща Охотника', 'Чистилище Нежити'), ('Безлюдная Пристань', 'Огненная Башня Хейда'), ('Бухта Брайтстоун-Тселдора', 'Личные Палаты Лорда'), ('Замок Дранглик', 'Королевский проход'), ('Большой собор', 'Ледяная Элеум Лойс'), ('Темнолесье', 'Храм Зимы'), ('Башня Солнца', 'Железная Цитадель'), ('Лес Павших Гигантов', 'Забытая Крепость'), ('Большой собор', 'Предвечный Хаос'), ('Забытая Крепость', 'Башня Луны'), ('Железная цитадель', 'Башня Солнца'), ('Забытая Крепость', 'Безлюдная Пристань'), ('Помойка', 'Черная Расселина'), ('Железная Цитадель', 'Мглистая Башня'), ('Святилище дракона', 'Убежище дракона'), ('Долина Жатвы', 'Земляной Пик'), ('Забытая Крепость', 'Холм Грешников'), ('Маджула', 'Роща Охотника'), ('Железная цитадель', 'Мглистая Башня'), ('Мглистая Башня', 'Железный проход'), ('Шульва, Священный город', 'Пещера мертвых'), ('Ледяная Элеум Лойс', 'Храм Зимы')}

    else:
        visited_locations = list()

        def print_transitions(url, title):
            # if len(visited_locations) >= 7:
            #     return

            if title in visited_locations:
                return

            visited_locations.append(title)
            # print(title, url)

            transitions = get_transitions_location(url)
            if not transitions:
                return transitions

            # # Сначала напечатаем все связанные локации
            # for url_trans, title_trans in transitions:
            #     print('    {} -> {}'.format(title_trans, url_trans))
            #
            # print('\n')

            # Поищем у этих локаций связаные с ними локации
            for url_trans, title_trans in transitions:
                # Проверяем что локации с обратной связью не занесены
                if (title_trans, title) not in global_transitions:
                    global_transitions.add((title, title_trans))

                print_transitions(url_trans, title_trans)

                # if title_trans not in visited_locations:
                #     # if len(global_transitions) >= 5:
                #     #     return
                #     #
                #     global_transitions.add((title, title_trans))
                #
                #     print_transitions(url_trans, title_trans)


        url_start_location = 'http://ru.darksouls.wikia.com/wiki/%D0%9C%D0%B5%D0%B6%D0%B4%D1%83%D0%BC%D0%B8%D1%80%D1%8C%D0%B5'
        print_transitions(url_start_location, 'Междумирье')

        print()
        print(len(visited_locations), visited_locations)

    # TODO: pretty graph
    import networkx as nx
    G = nx.Graph()

    print(global_transitions)
    for title, title_trans in global_transitions:
        # print('{} -> {}'.format(title, title_trans))
        G.add_edge(title, title_trans)

    print()

    pos = nx.spring_layout(G)  # positions for all nodes

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=6)

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=70)

    # labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')

    import matplotlib.pyplot as plt
    # plt.figure(1)
    plt.axis('off')
    # plt.savefig("ds2_locations_graph.png")  # save as png
    plt.show()  # display
