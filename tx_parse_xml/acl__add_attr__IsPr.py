#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from pathlib import Path
from bs4 import BeautifulSoup


FILE_NAME_ACL = Path(r'C:\<...>\ads\<...>\src\<...>.xml')

# NOTE: <Group Id="cpg<...>" Name="<...>" Members="<PROP_IDS">
PROP_IDS = "prd<...> prd<...>".split()

root_acl = BeautifulSoup(open(FILE_NAME_ACL, 'rb'), 'xml')

for prop_id in PROP_IDS:
    prop_el = root_acl.select_one(f'[Id="{prop_id}"]')

    if not prop_el.Presentation.has_attr('IsPresentable'):
        prop_el.Presentation['IsPresentable'] = 'false'

with open(FILE_NAME_ACL, 'w', encoding='utf-8') as f:
    f.write(str(root_acl))
