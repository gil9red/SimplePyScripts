#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def print_pretty_table(data, cell_sep=' | '):
    rows = len(data)
    cols = len(data[0])

    col_width = []
    for col in range(cols):
        columns = [data[row][col] for row in range(rows)]
        col_width.append(len(max(columns, key=len)))

    for row in range(rows):
        result = []
        for col in range(cols):
            item = data[row][col].rjust(col_width[col])
            result.append(item)

        print(cell_sep.join(result))


if __name__ == '__main__':
    table_data = [
        ['FRUIT', 'PERSON', 'ANIMAL'],
        ['apples', 'Alice', 'dogs'],
        ['oranges', 'Bob', 'cats'],
        ['cherries', 'Carol', 'moose'],
        ['banana', 'David', 'goose'],
    ]

    print_pretty_table(table_data)
    #    FRUIT | PERSON | ANIMAL
    #   apples |  Alice |   dogs
    #  oranges |    Bob |   cats
    # cherries |  Carol |  moose
    #   banana |  David |  goose
