#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from collections import defaultdict
from pathlib import Path
from typing import Union

import xml.etree.ElementTree as ET


# NOTE: ExcludeTargetDatabases еще присутствует во множестве объектов таблицы: индексы, триггеры, столбцы и т.п.
#       Но текущая реализация выводит только таблицы


def get_tables(model_path: Path) -> list[str]:
    ns = dict(
        dds='http://schemas.radixware.org/ddsdef.xsd',
    )

    items = []
    model = ET.fromstring(model_path.read_text(encoding='utf-8'))
    for table in model.findall('.//dds:Tables/dds:Table', namespaces=ns):
        if table.attrib['ExcludeTargetDatabases']:
            title = f"{table.attrib['Name']}({table.attrib['Id']})"
            items.append(title)

    return items


def process(branch_dir: Union[Path, str]) -> dict[str, list[str]]:
    if isinstance(branch_dir, str):
        branch_dir = Path(branch_dir)

    layer_module_by_tables = defaultdict(list)

    for layer_dir in branch_dir.glob('*'):
        if not layer_dir.is_dir():
            continue

        layer_dds_dir = layer_dir / 'dds'
        if layer_dds_dir.is_dir():
            layer = layer_dir.name
            for model_xml in layer_dds_dir.glob('*/model.xml'):
                module = model_xml.parent.name

                for table in get_tables(model_xml):
                    key = f"{layer}/{module}"
                    layer_module_by_tables[key].append(table)

    return layer_module_by_tables


if __name__ == "__main__":
    path = r'C:\DEV__OPTT\trunk_optt'

    for key, tables in process(path).items():
        print(f'{key} ({len(tables)})')
        for i, table in enumerate(tables, 1):
            print(f'    {i}. {table}')
        print()
