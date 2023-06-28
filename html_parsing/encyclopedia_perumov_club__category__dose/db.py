#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as dt
import pathlib
import os
import shutil
import sys

from peewee import *

sys.path.append("../..")
from shorten import shorten


# Absolute file name
DB_FILE_NAME = str(pathlib.Path(__file__).resolve().parent / "database.sqlite")


def db_create_backup(backup_dir="backup"):
    os.makedirs(backup_dir, exist_ok=True)

    file_name = str(dt.datetime.today().date()) + ".sqlite"
    file_name = os.path.join(backup_dir, file_name)

    shutil.copy(DB_FILE_NAME, file_name)


# Ensure foreign-key constraints are enforced.
db = SqliteDatabase(DB_FILE_NAME, pragmas={"foreign_keys": 1})


class BaseModel(Model):
    class Meta:
        database = db


class Dossier(BaseModel):
    title = TextField()
    url = TextField(unique=True)
    date = DateField(default=dt.date.today)

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, title={self.title!r}, date={self.date}, "
            f"url={self.url!r}, total_items={len(self.items)})"
        )


class QuestionAnswer(BaseModel):
    dossier = ForeignKeyField(Dossier, backref="items")
    question_text = TextField()
    answer_text = TextField()

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, dossier_id={self.dossier.id}, "
            f"question_text={shorten(self.question_text)!r}), answer_text={shorten(self.answer_text)!r})"
        )


def add(url: str, title: str, date: dt.date, question_answer_pairs) -> bool:
    dossier, created = Dossier.get_or_create(title=title, url=url, date=date)
    if not created:
        return False

    for question_text, answer_text in question_answer_pairs:
        question_answer, _ = QuestionAnswer.get_or_create(
            dossier=dossier, question_text=question_text, answer_text=answer_text
        )

    db_create_backup()

    return True


def has(url: str) -> bool:
    return bool(
        Dossier.get_or_none(url=url)
    )


db.connect()
db.create_tables([Dossier, QuestionAnswer])


if __name__ == "__main__":
    dossiers = Dossier.select()
    if not dossiers:
        print("Empty database!")
        sys.exit()

    print(f"Total dossiers:", len(dossiers))
    print(f"Total items:", sum(len(x.items) for x in dossiers))
    print()

    dossier = Dossier.select().first()
    print(dossier)
    # Dossier(id=1, title='Досье: Вампиры', date=2017-04-08, url='http://encyclopedia.perumov.club/vampiry-2/', total_items=5)

    for i, x in enumerate(dossier.items, 1):
        print(f"{i}. {x}")
    # 1. QuestionAnswer(id=1, dossier_id=1, question_text='Вот, к примеру, Вы сказали, чт...') answer_text='В случае с Эфраимом я согласен...')
    # 2. QuestionAnswer(id=2, dossier_id=1, question_text='Скажите пожалуйста, Капитан, в...') answer_text='Показ этих чувств необходим дл...')
    # 3. QuestionAnswer(id=3, dossier_id=1, question_text='Ник, скажите, а вампир может о...') answer_text='Вампир без крови обходиться не...')
    # 4. QuestionAnswer(id=4, dossier_id=1, question_text='Николай Данилович! Вы писали, ...') answer_text='Эфраим, как и все вампиры И ТА...')
    # 5. QuestionAnswer(id=5, dossier_id=1, question_text='Тут у нас возник очень острый ...') answer_text='Предательство Эйвилль — это не...')

    # print()
    #
    # search_text = "Спаситель".lower()
    # result_items = QuestionAnswer.select().where(
    #     fn.Lower(QuestionAnswer.question_text).contains(search_text)
    #     | fn.Lower(QuestionAnswer.answer_text).contains(search_text)
    # ).order_by(QuestionAnswer.dossier)
    # print(result_items)
    # print(f'Search for {search_text!r}, result: {len(result_items)}')
    #
    # for x in result_items:
    #     print(x)
