#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from common import get_transitions_location


# NOTE: Способ поиска локаций, начиная с начальной и через переходы локаций искать другие сработал, однако
# часть локаций потерялись -- не всегда на одной странице локации указывает переход на следующую, но это
# может быть в обратную сторону
# Поэтому, для большей надежности лучше использовать скрипт Dark_Souls_II__print_locations.py

def print_transitions(url: str, title: str, visited_locations: set, global_transitions: set, log=True):
    title = title.strip().title()
    if title in visited_locations:
        return

    log and print(title, url)
    visited_locations.add(title)

    transitions = get_transitions_location(url)
    if not transitions:
        return transitions

    transitions = [(url, title.title()) for url, title in transitions]

    if log:
        # Сначала напечатаем все связанные локации
        for url_trans, title_trans in transitions:
            print('    {} -> {}'.format(title_trans, url_trans))

        print()

    # Поищем у этих локаций связанные с ними локации
    for url_trans, title_trans in transitions:
        # Проверяем что локации с обратной связью не занесены
        if (title_trans, title) not in global_transitions:
            global_transitions.add((title, title_trans))

        print_transitions(url_trans, title_trans, visited_locations, global_transitions, log)


if __name__ == '__main__':
    visited_locations = set()
    global_transitions = set()

    url_start_location = 'http://ru.darksouls.wikia.com/wiki/Междумирье'
    print_transitions(url_start_location, 'Междумирье', visited_locations, global_transitions)

    print()
    print(len(visited_locations), sorted(visited_locations))
    print(len(global_transitions), sorted(global_transitions))
