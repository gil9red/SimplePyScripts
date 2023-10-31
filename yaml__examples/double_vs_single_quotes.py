#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install PyYAML
import yaml


data = yaml.safe_load(r"""
double: "123\n456"
single: '123\n456'
""")

import json
print(json.dumps(data, indent=4, ensure_ascii=False))
r"""
{
    "double": "123\n456",
    "single": "123\\n456"
}
"""