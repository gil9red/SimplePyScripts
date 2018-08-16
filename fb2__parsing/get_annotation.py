#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from bs4 import BeautifulSoup


def get_annotation(file_name: str) -> str:
    with open(file_name, encoding='utf-8') as f:
        root = BeautifulSoup(f, 'html.parser')

    annotation_node = root.select_one('description > title-info > annotation')
    if not annotation_node:
        return ''

    return annotation_node.text.strip()


if __name__ == '__main__':
    import glob
    import os

    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for fb2_file_name in glob.glob('input/*.fb2'):
        print(fb2_file_name)

        annotation = get_annotation(fb2_file_name)
        print(repr(annotation))
        print(annotation)

        print('\n')
