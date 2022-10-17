#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))
from root_common import session


url = 'https://helpdesk.compassluxe.com/rest/api/latest/user/avatars?username=ipetrash'

rs = session.get(url)
print(rs)
for kind, avatars in rs.json().items():
    print(f'{kind} ({len(avatars)}):')
    for item in avatars:
        print(f'    {item}')
