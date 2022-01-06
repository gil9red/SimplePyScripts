#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://www.saule-spb.ru/library/autorun.html
# SOURCE: http://datadump.ru/virus-detection/
# SOURCE: https://rsdn.org/article/baseserv/winlogon.xml
# SOURCE: https://www.saule-spb.ru/library/vx/look2mereg.html


from typing import Dict
from common import get_entries_as_dict, get_subkeys


PATH = r'HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\Notify'


def get_winlogon_notify() -> Dict[str, Dict[str, str]]:
    return {
        sub_key_name: get_entries_as_dict(sub_key, raw_value=True)
        for sub_key_name, sub_key in get_subkeys(PATH)
    }


if __name__ == '__main__':
    print(get_winlogon_notify())
