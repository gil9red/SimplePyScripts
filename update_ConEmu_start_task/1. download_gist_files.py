#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import re

from collections import defaultdict
from urllib.parse import urljoin
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from config import GIST_URL, DIR_GIST_FILES


DEBUG_LOG = False


# Clear directory
for file_name in DIR_GIST_FILES.glob('*'):
    file_name.unlink()

rs = requests.get(GIST_URL)
root = BeautifulSoup(rs.content, 'html.parser')

a_all = root.find('a', {"href": re.compile(r'/raw/.+/all\.txt')})
url_all = urljoin(rs.url, a_all['href'])

rs = requests.get(url_all)

group: str = ''
group_by_lines = defaultdict(list)
for line in rs.text.splitlines():
    if not line:
        continue
    elif line.startswith('# IGNORED'):
        break
    elif m := re.search(r'# GROUP (\d+)', line):
        group = m.group(1)
        if group in group_by_lines:
            raise Exception(f'Duplicate of group = {group!r}')
        continue
    elif line.startswith('#'):
        continue

    DEBUG_LOG and print(line)
    m = re.search(r'[a-z]:[^:]+\.py', line, flags=re.IGNORECASE)
    script_dir_path = Path(m.group()).parent

    line = line.replace('d:_', f'd:{script_dir_path}').replace('t:_', f't:[{group}]')
    DEBUG_LOG and print(line)

    if not group:
        raise Exception('"# GROUP" must be defined!')

    group_by_lines[group].append(line + '\n')
    DEBUG_LOG and print()

# Save to files
for group, lines in group_by_lines.items():
    gist_file = DIR_GIST_FILES / f'group{group}'
    gist_file.write_text('\n'.join(lines), 'utf-8')
