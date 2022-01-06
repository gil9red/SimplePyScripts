#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://www.saule-spb.ru/library/autorun.html
# SOURCE: http://datadump.ru/virus-detection/


from typing import Dict
from common import get_entry, get_subkeys


PATHS = [
    (r"HKLM\SYSTEM\CurrentControlSet\Services\WinSock2\Parameters\NameSpace_Catalog5", "DisplayString"),
    (r"HKLM\SYSTEM\CurrentControlSet\Services\WinSock2\Parameters\Protocol_Catalog9", "ProtocolName"),
]


def get_winsock_providers() -> Dict[str, str]:
    path_by_value = dict()
    for path, name in PATHS:
        for catalog in ['Catalog_Entries', 'Catalog_Entries64']:
            for sub_key_name, sub_key in get_subkeys(fr'{path}\{catalog}'):
                abs_path = fr'{path}\{catalog}\{sub_key_name}'
                entry = get_entry(abs_path, name)
                if entry and entry.value:
                    path_by_value[abs_path] = entry.value

    return path_by_value


if __name__ == '__main__':
    print(get_winsock_providers())
