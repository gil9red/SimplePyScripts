#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://helgeklein.com/blog/active-setup-explained/
#         https://windowsnotes.ru/registry-2/active-setup/
#         https://ru.stackoverflow.com/a/1351313/201445


from dataclasses import dataclass, field
from typing import Any

from common import RegistryKey


PATHS = [
    r"HKLM\Software\Microsoft\Active Setup\Installed Components",
    r"HKLM\Software\Wow6432Node\Microsoft\Active Setup\Installed Components",
    r"HKCU\Software\Microsoft\Active Setup\Installed Components",
    r"HKCU\Software\Wow6432Node\Microsoft\Active Setup\Installed Components",
]


@dataclass
class Component:
    guid: str
    default: str = ""
    is_installed: bool = True
    locale: str = ""
    stub_path: str = ""
    version: str = ""
    other_fields: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(cls, guid: str, fields: dict[str, Any]) -> "Component":
        return cls(
            guid=guid,
            default=fields.pop("", ""),
            is_installed=fields.pop("IsInstalled", True),
            locale=fields.pop("Locale", ""),
            stub_path=fields.pop("StubPath", ""),
            version=fields.pop("Version", ""),
            other_fields=fields,
        )


def get_active_setup_components(exists_stub_path=True) -> dict[str, list[Component]]:
    path_by_items = dict()

    for path in PATHS:
        key = RegistryKey(path)
        path = key.path

        if path not in path_by_items:
            path_by_items[path] = []

        for sub_key in key.subkeys():
            component = Component.create(
                sub_key.name,
                sub_key.get_str_values_as_dict(),
            )

            # Если задана проверка наличия stub_path и он пустой
            if exists_stub_path and not component.stub_path.strip():
                continue

            path_by_items[path].append(component)

    return path_by_items


if __name__ == "__main__":

    def _print_this(path_by_components: dict[str, list[Component]]) -> None:
        for path, components in path_by_components.items():
            print(f"{path} ({len(components)}):")
            for component in components:
                print(f"    {component}")

            print()

    path_by_components = get_active_setup_components()
    _print_this(path_by_components)

    print("\n" + "-" * 100 + "\n")

    path_by_components = get_active_setup_components(exists_stub_path=False)
    _print_this(path_by_components)
