#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# FFXIII-2
# clock solver

from copy import deepcopy


def is_win(clock_data) -> bool:
    return all(x == 0 for x in clock_data['items'])


def get_arrows_value(clock_data) -> (int, int):
    items = clock_data['items']
    arrow_1 = clock_data['left_arrow_index']
    arrow_2 = clock_data['right_arrow_index']

    return items[arrow_1], items[arrow_2]


def is_fail(clock_data) -> bool:
    a, b = get_arrows_value(clock_data)
    return a == 0 and b == 0


def click_clock_item(clock_data, selected_index: int):
    items = clock_data['items']
    move_value = items[selected_index]

    clock_data['selected_indexes'].append(selected_index)
    clock_data['selected_values'].append(move_value)

    # Кнопка активирована
    items[selected_index] = 0

    # Остаток по модулю поможет получить индекс после вращения стрелки по часовой или против
    left_arrow_index = (selected_index - move_value) % len(items)
    right_arrow_index = (selected_index + move_value) % len(items)

    clock_data['left_arrow_index'] = left_arrow_index
    clock_data['right_arrow_index'] = right_arrow_index


#       2
#    4     4
#   1        1
# 2           3
#   5      4
#       3
clock_items = [2, 4, 1, 3, 4, 3, 5, 2, 1, 4]

clock_data = {
    'items': deepcopy(clock_items),
    'history': [deepcopy(clock_items)],
    'left_arrow_index': 0,
    'right_arrow_index': 0,
    'selected_indexes': [],
    'selected_values': [],
}
# print(clock_data)
# print(get_arrows_value(clock_data))


RESULT_WIN = []


def foo(clock_data, index):
    clock_data = deepcopy(clock_data)

    if is_win(clock_data):
        # TODO: Save current <clock_data> in <results>
        # print('WIN!')
        # RESULT_WIN.append(copy(clock_data))
        RESULT_WIN.append(clock_data)
        return

    if is_fail(clock_data):
        # print('FAIL!')
        # nothing
        return

    click_clock_item(clock_data, index)

    # После клика изменятся часов, поэтому нужно сохранить это в истории
    clock_data['history'].append(deepcopy(clock_data['items']))

    # if is_win(clock_data):
    #     # TODO: Save current <clock_data> in <results>
    #     # print('WIN!')
    #     RESULT_WIN.append(copy(clock_data))
    #     return
    #
    # if is_fail(clock_data):
    #     # print('FAIL!')
    #     # nothing
    #     return

    arrow_1 = clock_data['left_arrow_index']
    foo(clock_data, arrow_1)

    arrow_2 = clock_data['right_arrow_index']
    foo(clock_data, arrow_2)


items = clock_data['items']

for index in range(len(items)):
    foo(clock_data, index)

print(len(RESULT_WIN))
for i, clock_data in enumerate(RESULT_WIN, 1):
    print(f'{i}.')

    for item, index, value in zip(clock_data['history'], clock_data['selected_indexes'], clock_data['selected_values']):
        print(f'{item} -> #{index} ({value})')

    print()
