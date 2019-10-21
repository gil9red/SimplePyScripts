#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import ast
from typing import AnyStr

# pip install astunparse
import astunparse


def clear_code(
        text: AnyStr,
        remove_meta_headers=True,
        meta_headers=(
            '__author__', '__copyright__', '__credits__', '__license__', '__version__',
            '__maintainer__', '__email__', '__status__'
        )
    ) -> str:
    tree = ast.parse(text)

    if remove_meta_headers:
        for node in ast.walk(tree):
            # Remove line likes "__author__ = 'ipetrash'"
            if isinstance(node, ast.Assign) and node.targets and isinstance(node.targets[0], ast.Name):
                if node.targets[0].id in meta_headers:
                    tree.body.remove(node)

    return astunparse.unparse(tree)


def clear_file(file_name: str, new_file_name: str = None, encoding='utf-8'):
    if new_file_name is None:
        new_file_name = file_name

    with open(file_name, encoding=encoding) as f:
        text = clear_code(f.read())

    with open(new_file_name, 'w', encoding=encoding) as f:
        f.write(text)


if __name__ == '__main__':
    with open(__file__, 'rb') as f:
        print(clear_code(f.read()))

    clear_file(__file__, __file__ + '.clear.py')
