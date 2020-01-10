#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import json
from pathlib import Path

import sys
sys.path.append('..')

from db import Dump

from playhouse.shortcuts import model_to_dict


DIR = Path(__file__).parent.resolve() / 'data'
DIR.mkdir(parents=True, exist_ok=True)

FILE_NAME_EXPORT_JSON = DIR / 'games.json'


if __name__ == '__main__':
    items = [model_to_dict(dump) for dump in Dump.select()]
    print(len(items))

    json.dump(
        items,
        open(FILE_NAME_EXPORT_JSON, 'w', encoding='utf-8'),
        ensure_ascii=False,
        indent=4
    )
