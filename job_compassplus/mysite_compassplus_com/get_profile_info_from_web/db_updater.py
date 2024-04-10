#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys

import db

from config import DIR
sys.path.append(str(DIR.parent))
from get_person_info import get_person_info, do_get


# TODO: Проверять поля на изменения и добавлять новую запись, если поменялось
def add_or_get_db(name: str) -> db.Person:
    person = db.Person.get_last_by_name(name)
    if person:
        return person

    info = get_person_info(name)
    return db.Person.create(
        name=info.name,
        position=info.position,
        department=info.department,
        img=do_get(info.img_url).content,
        location=info.location,
        birthday=info.birthday,
    )
