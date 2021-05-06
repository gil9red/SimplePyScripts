#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def pretty_table(data, cell_sep=' | ', header_separator=True) -> str:
    rows = len(data)
    cols = len(data[0])

    col_width = []
    for col in range(cols):
        columns = [str(data[row][col]) for row in range(rows)]
        col_width.append(len(max(columns, key=len)))

    separator = "-+-".join('-' * n for n in col_width)

    lines = []

    for i, row in enumerate(range(rows)):
        result = []
        for col in range(cols):
            item = str(data[row][col]).ljust(col_width[col])
            result.append(item)

        lines.append(cell_sep.join(result))

        if i == 0 and header_separator:
            lines.append(separator)

    return '\n'.join(lines)


def print_pretty_table(data, cell_sep=' | ', header_separator=True):
    print(pretty_table(data, cell_sep, header_separator))


if __name__ == '__main__':
    table_data = [
        ['FRUIT', 'PERSON', 'ANIMAL'],
        ['apples', 'Alice', 'dogs'],
        ['oranges', 'Bob', 'cats'],
        ['cherries', 'Carol', 'moose'],
        ['banana', 'David', 'goose'],
    ]

    print_pretty_table(table_data, header_separator=False)
    # FRUIT    | PERSON | ANIMAL
    # apples   | Alice  | dogs
    # oranges  | Bob    | cats
    # cherries | Carol  | moose
    # banana   | David  | goose

    print()

    print_pretty_table(table_data)
    # FRUIT    | PERSON | ANIMAL
    # ---------+--------+-------
    # apples   | Alice  | dogs
    # oranges  | Bob    | cats
    # cherries | Carol  | moose
    # banana   | David  | goose

    print()

    print_pretty_table([['FRUIT', 'PERSON', 'ANIMAL']])
