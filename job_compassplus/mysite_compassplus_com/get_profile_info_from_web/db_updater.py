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
from get_person_info import Person, get_person_info, get_jira_user_active


def create_person_from_info(info: Person) -> db.Person:
    return db.Person.create(
        name=info.name,
        position=info.position,
        department=info.department,
        img=info.download_img(),
        location=info.location,
        birthday=info.birthday,
        is_active=info.is_active,
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

    if person.birthday != info.birthday:
        return False

    if person.is_active != info.is_active:
        return False

    return True


def is_need_to_check(person: db.Person, d: date) -> bool:
    return d > person.last_check_date + timedelta(days=MAX_LAST_CHECK_DATE_DAYS)


def add_or_get_db(name: str, forced: bool = False) -> db.Person | None:
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
    if is_need_to_check(person, d=today) or forced:
        info = get_person_info(name)
        if info:
            if is_person_eq_info(person, info):
                person.last_check_date = today
                person.save()
            else:
                # Создание новой записи с актуальными полями
                person = create_person_from_info(info)

        else:  # Если пользователь был в БД, а потом его удалили из mysite
            # Создание новой записи
            return db.Person.create(
                name=person.name,
                position=person.position,
                department=person.department,
                img=person.img,
                location=person.location,
                birthday=person.birthday,
                is_active=False,
            )

    return person


def do_update_db(forced: bool = False):
    prefix: str = "[do_update_db]"

    print(f"{prefix} Start")

    while True:
        print(f"{prefix} Check all")
        try:
            # Запрос для получения ников
            query = db.Person.select(db.Person.name).distinct()
            names: list[str] = [x.name for x in query]
            for i, name in enumerate(names, 1):
                print(f"{prefix} Check {name} ({i}/{len(names)})")

                person: db.Person | None = None
                try:
                    person = add_or_get_db(name, forced=forced)
                except Exception as e:
                    print(f"{prefix} Error: {e}")
                finally:
                    # Оптимизация, чтобы не делать лишней задержку, если не было запроса по сети в add_or_get_db
                    # (это косвенно можно понять по last_check_date)
                    if not forced and person and not is_need_to_check(person, d=date.today()):
                        continue

                    time.sleep(10)

        except Exception:
            # Выводим ошибку в консоль
            tb = traceback.format_exc()
            print(f"{prefix} Error:\n{tb}")

        finally:
            time.sleep(24 * 60 * 60)  # Раз в сутки


if __name__ == "__main__":
    print(add_or_get_db("ipetrash"))

    # do_update_db(forced=True)
