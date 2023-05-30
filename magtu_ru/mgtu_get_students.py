#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests


rs = requests.get(
    "http://magtu.ru/modules/mod_reiting/mobile.php?action=get_all_department"
)

for dep in rs.json():
    id_dep = list(dep.keys())[0]
    name = dep[id_dep]
    print(id_dep, name)

    rs = requests.get(
        f"http://magtu.ru/modules/mod_reiting/mobile.php?action=get_spec_by_depart&depart_kod={id_dep}"
    )
    for kaf in rs.json():
        id_kaf = list(kaf.keys())[0]
        name = kaf[id_kaf]
        print("  " + id_kaf, name)

        rs = requests.get(
            f"http://magtu.ru/modules/mod_reiting/mobile.php?action=get_reiting&spec_kod={id_kaf}"
        )
        for i, stud in enumerate(rs.json(), 1):
            name = stud[0]
            print(f"    {i}. {name}")

        print()

    print()
