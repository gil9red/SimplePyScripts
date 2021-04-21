#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from collections import defaultdict
from pathlib import Path

from bs4 import BeautifulSoup


path_dir = Path(r'C:\DEV__TX\trunk_tx')
path_branch = path_dir / r'branch.xml'

# Сбор названий модулей из всех слоев
module_id_by_name = dict()

for file_module in path_dir.glob('*/ads/*/module.xml'):
    root = BeautifulSoup(file_module.read_bytes(), 'html.parser')
    module_root = root.select_one('Module')
    module_id = module_root['id']
    module_name = module_root['name']

    module_id_by_name[module_id] = module_name

root = BeautifulSoup(path_branch.read_bytes(), 'html.parser')
owner_by_modules = defaultdict(set)

for module_el in root.select('ModulesInfo > ModuleInfo'):
    layer_url = module_el.select_one('LayerUrl').get_text(strip=True)
    module_id = module_el.select_one('ModuleId').get_text(strip=True)

    module_name = module_id_by_name[module_id]
    full_module_name = f'{layer_url}/{module_name}'

    for owner_el in module_el.select('OwnerEmail'):
        owner = owner_el.get_text(strip=True)
        owner_by_modules[owner].add(full_module_name)

for owner, modules in sorted(owner_by_modules.items()):
    print(f'{owner} ({len(modules)}):')
    for x in sorted(modules):
        print(f'    {x}')

    print()
