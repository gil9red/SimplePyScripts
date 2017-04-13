#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Reducing the number of row in rows.

Скрипт для уменьшение количество элементов <row> в xml.

"""


if __name__ == '__main__':
    # NOTE: справочники CONTACT хранятся в кодировке cp1251 (windows-1251)

    import glob
    for file_name in glob.glob('mini_contact_dicts/*.xml'):
        print(file_name)

        from bs4 import BeautifulSoup
        root = BeautifulSoup(open(file_name, 'rb'), 'lxml', from_encoding='cp1251')

        rows = root.select('row')
        old_len = len(rows)

        for row in rows[20:]:
            row.decompose()

        rows = root.select('row')
        print('  len {} -> {}'.format(old_len, len(rows)))

        import os
        file_name = 'mini_contact_dicts/' + os.path.basename(file_name)

        with open(file_name, 'w', encoding='cp1251') as f:
            f.write(str(root))

        print('  Write to {}'.format(file_name))
        print()
