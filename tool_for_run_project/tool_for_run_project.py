#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
import sys


NAME_BY_PATH = {
    'optt': 'C:/DEV__OPTT',
    'tx':   'C:/DEV__TX',
}

WHAT_BY_FILE = {
    'designer': '!!designer.cmd',
    'explorer': '!!explorer.cmd',
    'server': '!!server.cmd',
}

if len(sys.argv) == 1 or len(sys.argv) != 4:
    print('''\
Run: <name> <version> <what>.
Example:
    optt trunk designer
    tx 3.2.6 server
''')
    quit()

name, version, what = map(str.lower, sys.argv[1:])

if version == 'trunk':
    version += '_' + name

dir_file_name = NAME_BY_PATH[name] + '/' + version
file_name = dir_file_name + '/' + WHAT_BY_FILE[what]

# Move to active dir
os.chdir(os.path.dirname(dir_file_name))

# Run
os.startfile(file_name)
