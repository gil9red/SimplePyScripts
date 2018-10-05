#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
import sys
import re
import pathlib


NAME_BY_PATH = {
    'optt': 'C:/DEV__OPTT',
    'tx':   'C:/DEV__TX',
}

WHAT_BY_FILE = {
    'designer': '!!designer.cmd',
    'd': '!!designer.cmd',

    'explorer': '!!explorer.cmd',
    'e': '!!explorer.cmd',

    'server': '!!server.cmd',
    's': '!!server.cmd',
}

argc = len(sys.argv)

if argc == 1 or (argc != 4 and argc != 2):
    print('''\
Run: <name> <version> <what>  -- Run tool
Run: <name>                   -- Print versions
Example:
  > optt trunk designer
  > tx 3.2.6 server
  > optt
    Version: ['2.1.7.1', 'trunk_optt']
''')
    quit()

if argc == 4:
    name, version, what = map(str.lower, sys.argv[1:])

    if version == 'trunk':
        version += '_' + name

    dir_file_name = NAME_BY_PATH[name] + '/' + version
    file_name = dir_file_name + '/' + WHAT_BY_FILE[what]

    print(f'Run: "{file_name}"')

    # Move to active dir
    os.chdir(dir_file_name)

    # Run
    os.startfile(file_name)

elif argc == 2:
    name = sys.argv[1].lower()
    name = NAME_BY_PATH[name]

    dirs = []

    for path in pathlib.Path(name).iterdir():
        if not path.is_dir():
            continue

        path = path.name

        if path.startswith('trunk_') or re.search('\d+(\.\d+)+', path):
            dirs.append(path)

    print('Version:', dirs)
