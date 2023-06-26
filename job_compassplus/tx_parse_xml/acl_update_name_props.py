#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from pathlib import Path
from bs4 import BeautifulSoup


FILE_NAME_ACL = Path(r'C:\DEV__TX\trunk_tx\com.tranzaxis\ads\Interfacing.W4\src\aclTJQ2GCOP7NFZPERU23FQA76GXQ.xml')

ITEMS = [
    ...
]

root_acl = BeautifulSoup(open(FILE_NAME_ACL, 'rb'), 'xml')
root_acl_str = str(root_acl)

for license_name, license_id, prop_name, prop_id in ITEMS:
    print(license_name, license_id, prop_name, prop_id)

    prop_el = root_acl.select_one(f'[Id="{prop_id}"]')
    old_prop_el_str = str(prop_el)

    prop_el['Name'] = f"{prop_name}_{license_id}"
    new_prop_el_str = str(prop_el)

    root_acl_str = root_acl_str.replace(old_prop_el_str, new_prop_el_str)

with open('new_' + FILE_NAME_ACL.name, 'w', encoding='utf-8') as f:
    f.write(root_acl_str)
