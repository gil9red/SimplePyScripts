#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Union

import xml.etree.ElementTree as ET


@dataclass
class Trigger:
    table_name: str
    name: str
    db_name: str


def get_triggers(model_path: Path) -> list[Trigger]:
    ns = dict(
        dds='http://schemas.radixware.org/ddsdef.xsd',
    )

    items = []
    model = ET.fromstring(model_path.read_text(encoding='utf-8'))
    for table in model.findall('.//dds:Tables/dds:Table', namespaces=ns):
        for trigger in table.findall('./dds:Triggers/dds:Trigger', namespaces=ns):
            if trigger.attrib.get('Type'):  # При True - триггер был создан автоматически радиксом
                continue

            items.append(Trigger(
                table_name=table.attrib['Name'],
                name=trigger.attrib['Name'],
                db_name=trigger.attrib['DbName'],
            ))

    return items


def process(branch_dir: Union[Path, str]) -> dict[str, list[Trigger]]:
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

                for trigger in get_triggers(model_xml):
                    key = f"{layer}/{module}"
                    layer_module_by_triggers[key].append(trigger)

    return layer_module_by_triggers


if __name__ == "__main__":
    path = r'C:\DEV__OPTT\trunk_optt'

    layer_module_by_triggers = process(path)
    for key, triggers in layer_module_by_triggers.items():
        print(f'{key} ({len(triggers)})')
        for i, trigger in enumerate(triggers, 1):
            print(f'    {i}. {trigger.table_name}. {trigger.name} ({trigger.db_name})')
        print()
