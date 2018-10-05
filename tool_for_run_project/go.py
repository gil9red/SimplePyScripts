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

if argc == 1:
    print('''\
Run: <name> <version> <what>  -- Run tool
Run: <name> <version>         -- Open dir version
Run: <name> open              -- Open dir
Run: <name>                   -- Print versions
Example:
  > optt trunk designer
    Run: "C:/DEV__OPTT/trunk_optt/!!designer.cmd"
    
  > tx 3.2.6.10 server
    Run: "C:/DEV__TX/3.2.6.10/!!server.cmd"
  
  > optt trunk
    Open: "C:/DEV__OPTT/trunk_optt"
   
  > optt open
    Open: "C:/DEV__OPTT"
    
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

elif argc == 3:
    name, version = map(str.lower, (sys.argv[1], sys.argv[2]))

    dir_file_name = NAME_BY_PATH[name]

    # Для команды open версия не нужна
    if version != 'open':
        if version == 'trunk':
            version += '_' + name

        dir_file_name += '/' + version

    print(f'Open: "{dir_file_name}"')

    # Open
    os.startfile(dir_file_name)

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
