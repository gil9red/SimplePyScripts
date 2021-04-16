#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
import sys
import re
from pathlib import Path
from typing import Optional, List, Tuple

NAME_BY_PATH = {
    'optt':    'C:/DEV__OPTT',
    'tx':      'C:/DEV__TX',
    'manager': 'C:/manager_1_2_11_23_8',
    'doc':     'C:/Program Files (x86)/DocFetcher',
}
NAME_BY_PATH['щзее'] = NAME_BY_PATH['optt']
NAME_BY_PATH['еч'] = NAME_BY_PATH['tx']
NAME_BY_PATH['ьфтфпук'] = NAME_BY_PATH['manager']
NAME_BY_PATH['вщс'] = NAME_BY_PATH['doc']

WHAT_BY_FILE = {
    'designer': '!!designer.cmd',
    'explorer': '!!explorer.cmd',
    'server':   '!!server.cmd',
}
WHAT_BY_FILE['вуышптук'] = WHAT_BY_FILE['designer']
WHAT_BY_FILE['учздщкук'] = WHAT_BY_FILE['explorer']
WHAT_BY_FILE['ыукмук'] = WHAT_BY_FILE['server']

ABOUT_TEXT = '''\
RUN:
  <name> <version> <what>  -- Run tool
  <name> <what>            -- Run tool (trunk version)
  open <name> <version>    -- Open dir version
  open <name>              -- Open dir
  <name>                   -- Print versions

SUPPORTED NAMES:
{}

SUPPORTED WHATS:
{}

EXAMPLES:
  > optt trunk designer
    Run: "C:/DEV__OPTT/trunk_optt/!!designer.cmd"
    
  > tx 3.2.6.10 server
    Run: "C:/DEV__TX/3.2.6.10/!!server.cmd"
  
  > go tx designer
    Run: "C:/DEV__TX/trunk_tx/!!designer.cmd"
  
  > open optt trunk
    Open: "C:/DEV__OPTT/trunk_optt"
   
  > open optt
    Open: "C:/DEV__OPTT"
    
  > optt
    Version: ['2.1.7.1', 'trunk_optt']
'''.format(
        '\n'.join('  {:<10} {}'.format(k, v) for k, v in sorted(NAME_BY_PATH.items())),
        '\n'.join('  {:<10} {}'.format(k, v) for k, v in sorted(WHAT_BY_FILE.items())),
    )


def get_similar_value(alias: str, items: list) -> Optional[str]:
    if alias in items:
        return alias

    # Ищем похожие ключи по начальной строке
    keys = [key for key in items if key.startswith(alias)]

    # Нашли одну вариацию -- подходит
    if len(keys) == 1:
        return keys[0]

    return


def has_similar_value(alias: str, items: list) -> bool:
    return get_similar_value(alias, items) is not None


# For NAME_BY_PATH
def get_name_by_path(alias: str) -> str:
    keys = list(NAME_BY_PATH)
    key = get_similar_value(alias, keys)
    if not key:
        raise Exception(f'Unknown key "{alias}", supported: {keys}')

    return NAME_BY_PATH[key]


# For NAME_BY_PATH
def get_similar_name(alias: str) -> str:
    return get_similar_value(alias, list(NAME_BY_PATH.keys()))


# For WHAT_BY_FILE
def has_what_by_file(alias: str):
    return has_similar_value(alias, list(WHAT_BY_FILE.keys()))


# For WHAT_BY_FILE
def get_what_by_file(alias: str) -> str:
    keys = list(WHAT_BY_FILE)
    key = get_similar_value(alias, keys)
    if not key:
        raise Exception(f'Unknown key "{alias}", supported: {keys}')

    return WHAT_BY_FILE[key]


def get_versions(alias: str) -> List[Tuple[str, str]]:
    name = get_name_by_path(alias)

    dirs = []

    for disc in 'CD':
        if not Path(disc + name[1:]).exists():
            continue

        for path in Path(disc + name[1:]).iterdir():
            if not path.is_dir():
                continue

            if path.name.startswith('trunk_') or re.search(r'\d+(\.\d+)+', path.name):
                dirs.append((path.name, str(path)))

    return dirs


def get_similar_version(name: str, alias: str) -> str:
    # Monkey patch
    def get_similar_value(alias: str, items: list) -> Optional[str]:
        for [base_dir, full_dir] in items:
            if alias == base_dir:
                return full_dir

        # Ищем похожие ключи по начальной строке
        keys = [full_dir for [base_dir, full_dir] in items if base_dir.startswith(alias)]

        # Нашли одну вариацию -- подходит
        if len(keys) == 1:
            return keys[0]

        return

    versions = get_versions(name)
    key = get_similar_value(alias, versions)
    if not key:
        raise Exception(f'Unknown version "{alias}", supported: {versions}')

    return key


def _run_file(file_name: str):
    dir_file_name = os.path.dirname(file_name)
    file_name = os.path.normpath(file_name)

    print(f'Run: "{file_name}"')

    # Move to active dir
    os.chdir(dir_file_name)

    # Run
    os.startfile(file_name)


def go_run(name: str, version: str, what: str):
    dir_file_name = get_similar_version(name, version)

    for what in what.split('+'):
        what = what.strip()

        file_name = dir_file_name + '/' + get_what_by_file(what)
        _run_file(file_name)


def go_open(name: str, version: str = ""):
    # Например: "o" -> "optt"
    dir_file_name = get_name_by_path(name)
    name = get_similar_name(name)

    if version:
        dir_file_name += '/' + get_similar_version(name, version)

    print(f'Open: "{dir_file_name}"')

    # Open
    os.startfile(dir_file_name)


def run_manager():
    dir_file_name = get_name_by_path('manager')
    file_name = dir_file_name + '/manager/bin/manager.cmd'
    _run_file(file_name)


def run_doc():
    dir_file_name = get_name_by_path('doc')
    file_name = dir_file_name + '/DocFetcher-8192_64-bit-Java.exe'
    _run_file(file_name)


def go_print_versions(alias: str):
    print('Version:', get_versions(alias))


if __name__ == '__main__':
    # Первый аргумент пропускаем -- это путь до текущего файла
    argv = list(map(str.lower, sys.argv[1:]))
    argc = len(argv)

    if argc == 0:
        print(ABOUT_TEXT)
        quit()

    elif argc == 1:
        name = argv[0]

        # У менеджера версий не бывает
        if 'manager'.startswith(name) or 'ьфтфпук'.startswith(name):
            run_manager()

        if 'doc'.startswith(name) or 'вщс'.startswith(name):
            run_doc()

        else:
            go_print_versions(name)

    elif argc == 2:
        name, alias = argv
        version = 'trunk'

        if name == 'open':
            go_open(name=alias)
        else:
            go_run(name, 'trunk', what=alias)

    elif argc == 3:
        name, version, what = argv

        if name == 'open':
            go_open(name=version, version=what)
        else:
            go_run(name, version, what)
