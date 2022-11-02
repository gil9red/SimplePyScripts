#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from collections import defaultdict
from pathlib import Path
from typing import Union

from bs4 import BeautifulSoup


def parse_xml_partially(path: Union[str, Path], line_contains: list) -> BeautifulSoup:
    # Считаем только ту часть XML, где имеются необходимые атрибуты
    xml_part = []
    for line in open(path, encoding='utf-8'):
        xml_part.append(line)
        if all(x in line for x in line_contains):
            break

    return BeautifulSoup('\n'.join(xml_part), 'html.parser')


def get_owner_by_modules(project_dir: Union[str, Path]) -> dict[str, list[str]]:
    if isinstance(project_dir, str):
        project_dir = Path(project_dir)

    layer_url_by_name: dict[str, str] = dict()
    layer_module_id_by_name: dict[tuple[str, str], str] = dict()

    for layer_path in project_dir.glob('*/layer.xml'):
        root_layer = parse_xml_partially(layer_path, line_contains=['Layer ', ' Uri', ' Name'])
        layer_url = root_layer.layer['uri']
        name = root_layer.layer['name']
        layer_url_by_name[layer_url] = name

        for path in layer_path.parent.glob('ads/*/module.xml'):
            root_module = parse_xml_partially(path, line_contains=['Module ', ' Id', ' Name'])
            module_id = root_module.module['id']

            layer_module_id_by_name[layer_url, module_id] = root_module.module['name']

    file_name_branch = project_dir / "branch.xml"

    with open(file_name_branch, encoding='utf-8') as f:
        root = BeautifulSoup(f, 'html.parser')

    owner_by_modules = defaultdict(list)

    for module in root.select('moduleinfo'):
        layer_url = module.layerurl.text
        module_id = module.moduleid.text

        owner_emails = [el.text for el in module.select('owneremail')]
        for email in owner_emails:
            layer_name = layer_url_by_name[layer_url]
            module_name = layer_module_id_by_name[layer_url, module_id]

            owner_by_modules[email].append(
                f'{layer_name}::{module_name} ({module_id})'
            )

    return owner_by_modules


if __name__ == '__main__':
    project_dir = "C:/DEV__TX/trunk_tx"
    owner_by_modules = get_owner_by_modules(project_dir)

    for email in sorted(owner_by_modules):
        modules = owner_by_modules[email]
        modules.sort()

        print(f'{email} ({len(modules)}):')
        for module in modules:
            print(f'    {module}')
        print()
