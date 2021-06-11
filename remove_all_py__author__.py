#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import re
import shutil

from pathlib import Path


TEMPLATE_DIR = 'No __author__ in {path}'


def process_file(file_name: Path):
    text = file_name.read_text('utf-8')
    text = re.sub(r'__author__ = .+', '', text)
    text = re.sub(r'\n{4,}', '\n\n\n', text)

    file_name.write_text(text, 'utf-8')


def run(path: str):
    path = Path(path)
    if not path.exists():
        raise Exception(f'Not found {path}!')

    if not path.is_dir():
        raise Exception(f'Must be directory: {path}!')

    dir_path = path.parent
    copy_dir_path = dir_path / (TEMPLATE_DIR.format(path=path.name))

    shutil.rmtree(copy_dir_path, ignore_errors=True)
    shutil.copytree(path, copy_dir_path)

    # Удалить из всех ее файлов указание автора
    for file_name in copy_dir_path.rglob('*.py'):
        process_file(file_name)


if __name__ == '__main__':
    run(r'C:\Users\ipetrash\PycharmProjects\SNMP_monitor')
