#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://www.saule-spb.ru/library/autorun.html
# SOURCE: http://datadump.ru/virus-detection/


from common import RegistryKey


PATHS = [
    (r"HKLM\SYSTEM\CurrentControlSet\Services\WinSock2\Parameters\NameSpace_Catalog5", "DisplayString"),
    (r"HKLM\SYSTEM\CurrentControlSet\Services\WinSock2\Parameters\Protocol_Catalog9", "ProtocolName"),
]


def get_winsock_providers() -> dict[str, str]:
    path_by_value = dict()
    for path, name in PATHS:
        for catalog in ['Catalog_Entries', 'Catalog_Entries64']:
            key = RegistryKey(path) / catalog
            for sub_key in key.subkeys():
                if value := sub_key.get_str_value(name):
                    path_by_value[sub_key.path] = value

    return path_by_value


if __name__ == '__main__':
    path_by_value = get_winsock_providers()
    print(path_by_value)
    print()

    for path, value in path_by_value.items():
        print(path, value)
        break
    # HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WinSock2\Parameters\NameSpace_Catalog5\Catalog_Entries\000000000001 @%SystemRoot%\system32\napinsp.dll,-1000
