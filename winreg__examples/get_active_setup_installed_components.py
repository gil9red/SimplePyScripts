#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://helgeklein.com/blog/active-setup-explained/
#         https://windowsnotes.ru/registry-2/active-setup/


from dataclasses import dataclass, field
from typing import Dict, Any, List

from common import get_subkeys, get_entries_as_dict


PATHS = [
    r'HKLM\Software\Microsoft\Active Setup\Installed Components',
    r'HKLM\Software\Wow6432Node\Microsoft\Active Setup\Installed Components',
    r'HKCU\Software\Microsoft\Active Setup\Installed Components',
    r'HKCU\Software\Wow6432Node\Microsoft\Active Setup\Installed Components',
]


@dataclass
class Component:
    guid: str
    default: str = ''
    is_installed: bool = True
    locale: str = ''
    stub_path: str = ''
    version: str = ''
    other_fields: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(cls, guid: str, fields: Dict[str, Any]) -> 'Component':
        return cls(
            guid=guid,
            default=fields.pop('', ''),
            is_installed=fields.pop('IsInstalled', True),
            locale=fields.pop('Locale', ''),
            stub_path=fields.pop('StubPath', ''),
            version=fields.pop('Version', ''),
            other_fields=fields,
        )


def get_active_setup_components(exists_stub_path=True) -> Dict[str, List[Component]]:
    path_by_items = dict()

    for path in PATHS:
        if path not in path_by_items:
            path_by_items[path] = []

        for sub_key_name, sub_key in get_subkeys(path):
            entries = get_entries_as_dict(sub_key, raw_value=True)
            component = Component.create(sub_key_name, entries)

            # Если задана проверка наличия stub_path и он пустой
            if exists_stub_path and not component.stub_path.strip():
                continue

            path_by_items[path].append(component)

    return path_by_items


if __name__ == '__main__':
    def _print_this(path_by_components: Dict[str, List[Component]]):
        for path, components in path_by_components.items():
            print(f'{path} ({len(components)}):')
            for component in components:
                print(f'    {component}')
                print([(k, v) for k, v in component.other_fields.items() if ' ' in k])

            print()

    path_by_components = get_active_setup_components()
    _print_this(path_by_components)

    print('\n' + '-' * 100 + '\n')

    path_by_components = get_active_setup_components(exists_stub_path=False)
    _print_this(path_by_components)
