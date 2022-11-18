#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Union

import xml.etree.ElementTree as ET


@dataclass
class View:
    id: str
    name: str
    db_name: str


def get_views(model_path: Path) -> list[View]:
    ns = dict(
        dds='http://schemas.radixware.org/ddsdef.xsd',
    )

    items = []
    model = ET.fromstring(model_path.read_text(encoding='utf-8'))
    for view in model.findall('.//dds:Views/dds:View', namespaces=ns):
        items.append(View(
            id=view.attrib['Id'],
            name=view.attrib['Name'],
            db_name=view.attrib['DbName'],
        ))

    return items


def process(branch_dir: Union[Path, str]) -> dict[str, list[View]]:
    if isinstance(branch_dir, str):
        branch_dir = Path(branch_dir)

    layer_module_by_triggers = defaultdict(list)

    for layer_dir in branch_dir.glob('*'):
        if not layer_dir.is_dir():
            continue

        layer_dds_dir = layer_dir / 'dds'
        if layer_dds_dir.is_dir():
            layer = layer_dir.name
            for model_xml in layer_dds_dir.glob('*/model.xml'):
                module = model_xml.parent.name

                for view in get_views(model_xml):
                    key = f"{layer}/{module}"
                    layer_module_by_triggers[key].append(view)

    return layer_module_by_triggers


if __name__ == "__main__":
    path = r'C:\DEV__OPTT\trunk_optt'

    layer_module_by_triggers = process(path)
    for key, views in layer_module_by_triggers.items():
        print(f'{key} ({len(views)})')
        for i, view in enumerate(views, 1):
            print(f'    {i}. {view.name} ({view.db_name}, {view.id})')
        print()
