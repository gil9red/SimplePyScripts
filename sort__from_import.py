#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def _sort_key(x: str):
    oper, *libs = x.split()
    return 0 if oper == 'import' else 1, libs


text = """
import json
from typing import List, Tuple
import re
import sys
from pathlib import Path
""".strip()


items = sorted(text.splitlines(), key=_sort_key)
print(
    *items, sep='\n'
)
"""
import json
import re
import sys
from pathlib import Path
from typing import List, Tuple
"""
