#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://www.saule-spb.ru/library/autorun.html
# SOURCE: http://datadump.ru/virus-detection/
# SOURCE: https://rsdn.org/article/baseserv/winlogon.xml
# SOURCE: https://www.saule-spb.ru/library/vx/look2mereg.html


from common import RegistryKey


PATH = r"HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\Notify"


def get_winlogon_notify() -> dict[str, dict[str, str]]:
    key = RegistryKey.get_or_none(PATH)
    subkeys = key.subkeys() if key else []

    return {
        sub_key.path: sub_key.get_str_values_as_dict()
        for sub_key in subkeys
    }


if __name__ == "__main__":
    print(get_winlogon_notify())
