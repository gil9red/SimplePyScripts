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
    CACHE = False
    if CACHE:
        global_transitions = {('Железная Цитадель', 'Мглистая Башня'), ('Шульва, Священный Город', 'Святилище Дракона'), ('Огненная Башня Хейда', 'Маджула'), ('Темнолесье', 'Цитадель Алдии'), ('Цитадель Алдии', 'Гнездо Дракона'), ('Замок Дранглик', 'Трон Желания'), ('Роща Охотника', 'Чистилище Нежити'), ('Шульва, Священный Город', 'Пещера Мертвых'), ('Святилище Дракона', 'Убежище Дракона'), ('Темнолесье', 'Двери Фарроса'), ('Бухта Брайтстоун-Тселдора', 'Личные Палаты Лорда'), ('Маджула', 'Могила Святых'), ('Склеп Нежити', 'Память Короля'), ('Мглистая Башня', 'Железный Проход'), ('Железная Цитадель', 'Башня Солнца'), ('Земляной Пик', 'Железная Цитадель'), ('Роща Охотника', 'Долина Жатвы'), ('Ледяная Элеум Лойс', 'Храм Зимы'), ('Помойка', 'Черная Расселина'), ('Бухта Брайтстоун-Тселдора', 'Воспоминания Дракона'), ('Могила Святых', 'Помойка'), ('Королевский Проход ', 'Замок Дранглик'), ('Большой Собор', 'Ледяная Элеум Лойс'), ('Маджула', 'Роща Охотника'), ('Мглистая Башня', 'Память Старого Железного Короля'), ('Безлюдная Пристань', 'Огненная Башня Хейда'), ('Ледяная Элеум Лойс', 'Холодные Окраины'), ('Храм Зимы', ' Ледяная Элеум Лойс'), ('Гнездо Дракона', 'Храм Дракона'), ('Большой Собор', 'Предвечный Хаос'), ('Храм Аманы', 'Склеп Нежити'), ('Долина Жатвы', 'Земляной Пик'), ('Забытая Крепость', 'Безлюдная Пристань'), ('Лес Павших Гигантов', 'Память Ваммара'), (' Ледяная Элеум Лойс', 'Большой Собор'), ('Черная Расселина', 'Шульва, Священный Город'), ('Междумирье', 'Маджула'), ('Замок Дранглик', 'Королевский Проход'), ('Храм Зимы', 'Замок Дранглик'), ('Маджула', 'Помойка'), ('Лес Павших Гигантов', 'Память Джейта'), ('Лес Павших Гигантов', 'Забытая Крепость'), ('Огненная Башня Хейда', 'Собор Лазурного Пути'), ('Лес Павших Гигантов', 'Память Орро'), (' Ледяная Элеум Лойс', 'Холодные Окраины'), ('Королевский Проход', 'Храм Аманы'), ('Храм Аманы', 'Королевский Проход '), ('Темнолесье', 'Храм Зимы'), ('Маджула', 'Темнолесье'), ('Маджула', 'Лес Павших Гигантов'), ('Забытая Крепость', 'Башня Луны'), ('Забытая Крепость', 'Холм Грешников'), ('Двери Фарроса', 'Бухта Брайтстоун-Тселдора')}

    else:
        visited_locations = set()

        def print_transitions(url, title):
            title = title.lower()

            # if len(visited_locations) >= 7:
            #     return

            if title in visited_locations:
                return

            visited_locations.add(title)
            # print(title.title(), url)

            transitions = get_transitions_location(url)
            if not transitions:
                return transitions

            # # Сначала напечатаем все связанные локации
            # for url_trans, title_trans in transitions:
            #     print('    {} -> {}'.format(title_trans.title(), url_trans))
            #
            # print('\n')

            # Поищем у этих локаций связаные с ними локации
            for url_trans, title_trans in transitions:
                title_trans = title_trans.lower()

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

        visited_locations = [_.title() for _ in visited_locations]
        global_transitions = {(_.title(), __.title()) for _, __ in global_transitions}

        print()
        print(len(visited_locations), visited_locations)

    print(len(global_transitions), global_transitions)

    # TODO: pretty graph
    import networkx as nx
    G = nx.Graph()

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
