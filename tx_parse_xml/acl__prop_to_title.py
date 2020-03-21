#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from pathlib import Path
from bs4 import BeautifulSoup

FILE_NAME_ACL = Path(r'C:\<...>\ads\<...>\src\<...>.xml')
FILE_NAME_ACL_LOCALE = FILE_NAME_ACL.parent.parent / 'locale' / 'en' / ('mlb' + FILE_NAME_ACL.name)

root_acl = BeautifulSoup(open(FILE_NAME_ACL, 'rb'), 'html.parser')
root_acl_locale = BeautifulSoup(open(FILE_NAME_ACL_LOCALE, 'rb'), 'html.parser')

# NOTE: <Group Id="cpg<...>" Name="<...>" Members="<PROP_IDS">
PROP_IDS = "prd<...> prd<...>".split()

items = []

for prop_id in PROP_IDS:
    prop_el = root_acl.select_one('#' + prop_id)
    name = prop_el['name']

    title_id = prop_el.presentation['titleid']
    title = root_acl_locale.select_one('#' + title_id).value.text

    items.append((name, title))

items.sort()

for name, title in items:
    print(name, title, sep='\t')
