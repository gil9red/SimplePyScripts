#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""Скрипт собирает вопросы с ru.stackoverflow, связанные с исключениями, но у которых нет метки "исключения"."""


import pickle
import time

import requests

from sqlalchemy import (
    create_engine,
    Table,
    Column,
    Integer,
    MetaData,
    DateTime,
    Boolean,
    literal,
)
from sqlalchemy.orm import mapper, sessionmaker

from main import get_logger


class Question:
    def __init__(self, id):
        self.id = id
        self.editable = False
        self.editable_date = None

    def __repr__(self):
        return f"<Question(#{self.id}. Editable: {self.editable}. Editable_date: {self.editable_date})>"

    @property
    def url(self):
        return "https://ru.stackoverflow.com/questions/" + str(self.id)


def get_session_factory():
    # Создаем базу, включаем логирование и автообновление подключения каждые 2 часа (7200 секунд)
    engine = create_engine(
        # 'sqlite:///:memory:',
        "sqlite:///questions.db",
        # echo=True,
        pool_recycle=7200,
    )

    metadata = MetaData()

    comments_table = Table(
        "Question",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("editable", Boolean),
        Column("editable_date", DateTime),
    )

    mapper(Question, comments_table)
    metadata.create_all(engine)

    return sessionmaker(bind=engine)


Session = get_session_factory()
session = Session()

query = session.query(Question)

logger = get_logger("gatherer")


def search_questions(title, body):
    page = 1

    questions = list()

    while True:
        params = {
            "site": "ru.stackoverflow",
            "nottagged": "исключения",
            "title": title,
            "body": body,
            "page": page,
        }

        rs = requests.get("https://api.stackexchange.com/2.2/search/advanced", params)
        logger.debug("Rs: %s, rs.url: %s", rs, rs.url)

        rs = rs.json()
        logger.debug("Rs.json: %s", rs)

        for item in rs["items"]:
            questions.append(item["question_id"])

        page += 1
        if not rs["has_more"]:
            break

        if rs["quota_remaining"] == 0:
            pickle.dump(questions, open(f"questions_{page}", "wb"))
            time.sleep(60 * 60 * 24 + 3600)

    return questions


def has_id(question_id):
    has_id = session.query(Question).filter(Question.id == question_id).exists()
    has_id = session.query(literal(True)).filter(has_id).scalar()
    return True == has_id


if __name__ == "__main__":
    questions = list()
    questions += search_questions("исключения", None)
    questions += search_questions("исключение", None)
    questions += search_questions("exception", None)
    questions += search_questions(None, "исключения")
    questions += search_questions(None, "исключение")
    questions += search_questions(None, "exception")

    for q in set(questions):
        if not has_id(q):
            logger.debug("Add question with id=%s.", q)
            session.add(Question(q))
        else:
            logger.debug("Question with id=%s exist.", q)

    session.commit()
