#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sqlite3

from config import URL_DS1, URL_DS2, URL_DS3
from utils import (
    get_bosses, print_bosses, convert_bosses_to_only_name,
    export_to_json, export_to_sqlite,
)


bosses_ds1 = get_bosses(URL_DS1)
print_bosses(URL_DS1, bosses_ds1)
export_to_json('dumps/ds1/bosses.json', bosses_ds1)
export_to_json('dumps/ds1/bosses__only_name.json', convert_bosses_to_only_name(bosses_ds1))

bosses_ds2 = get_bosses(URL_DS2)
print_bosses(URL_DS2, bosses_ds2)
export_to_json('dumps/ds2/bosses.json', bosses_ds2)
export_to_json('dumps/ds2/bosses__only_name.json', convert_bosses_to_only_name(bosses_ds2))

bosses_ds3 = get_bosses(URL_DS3)
print_bosses(URL_DS3, bosses_ds3)
export_to_json('dumps/ds3/bosses.json', bosses_ds3)
export_to_json('dumps/ds3/bosses__only_name.json', convert_bosses_to_only_name(bosses_ds3))

# All bosses
bosses_ds123 = {
    'Dark Souls':     bosses_ds1,
    'Dark Souls II':  bosses_ds2,
    'Dark Souls III': bosses_ds3,
}
export_to_json('dumps/bosses_ds123.json', bosses_ds123)

bosses_ds123__only_name = {
    'Dark Souls':     convert_bosses_to_only_name(bosses_ds1),
    'Dark Souls II':  convert_bosses_to_only_name(bosses_ds2),
    'Dark Souls III': convert_bosses_to_only_name(bosses_ds3),
}
export_to_json('dumps/bosses_ds123__only_name.json', bosses_ds123__only_name)

#
# SQLITE
#
sql_file_name = 'dumps/bosses_ds123.sqlite'
export_to_sqlite(sql_file_name, bosses_ds123)

# TEST
connect = sqlite3.connect(sql_file_name)
print('Total boss:',     connect.execute('SELECT count(*) FROM BOSS').fetchone()[0])
print('Total boss DS1:', connect.execute('SELECT count(*) FROM BOSS WHERE game = "Dark Souls"').fetchone()[0])
print('Total boss DS2:', connect.execute('SELECT count(*) FROM BOSS WHERE game = "Dark Souls II"').fetchone()[0])
print('Total boss DS3:', connect.execute('SELECT count(*) FROM BOSS WHERE game = "Dark Souls III"').fetchone()[0])
# Total boss: 92
# Total boss DS1: 26
# Total boss DS2: 41
# Total boss DS3: 25
