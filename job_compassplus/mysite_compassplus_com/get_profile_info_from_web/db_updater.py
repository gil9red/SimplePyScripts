#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import time
import traceback
from datetime import date, timedelta

import db

from config import DIR, MAX_LAST_CHECK_DATE_DAYS

sys.path.append(str(DIR.parent))
from get_person_info import Person, get_person_info


def create_person_from_info(info: Person) -> db.Person:
    return db.Person.create(
        name=info.name,
        position=info.position,
        department=info.department,
        img=info.download_img(),
        location=info.location,
        birthday=info.birthday,
    )


def is_person_eq_info(person: db.Person, info: Person) -> bool:
    if person.img != info.download_img():
        return False

    if person.department != info.department:
        return False

    if person.position != info.position:
        return False

    if person.location != info.location:
        return False

    if person.birthday != info.birthday:  # Мало ли, ошибка была
        return False

    return True


def add_or_get_db(name: str) -> db.Person | None:
    person = db.Person.get_last_by_name(name)

    # Если нет, то создать
    if not person:
        info = get_person_info(name)
        if not info:
            return
        return create_person_from_info(info)

    # Проверить дату проверку
    # Если с даты последней проверки прошло больше MAX_LAST_CHECK_DATE_DAYS дней, то
    # нужно проверить изменения полей
    today = date.today()
    if today > person.last_check_date + timedelta(days=MAX_LAST_CHECK_DATE_DAYS):
        info = get_person_info(name)
        if is_person_eq_info(person, info):
            person.last_check_date = today
            person.save()
        else:
            # Создание новой записи с актуальными полями
            person = create_person_from_info(info)

    return person


def do_update_db():
    print("[do_update_db] Start")

    while True:
        print("[do_update_db] Check")
        try:
            # Запрос для получения ников
            query = db.Person.select(db.Person.name).distinct()
            names: list[str] = [x.name for x in query]
            for name in names:
                add_or_get_db(name)
                time.sleep(10)

        except Exception:
            # Выводим ошибку в консоль
            tb = traceback.format_exc()
            print(f"[do_update_db] Error:\n{tb}")

        finally:
            time.sleep(24 * 60 * 60)  # Раз в сутки


if __name__ == "__main__":
    print(add_or_get_db("ipetrash"))
