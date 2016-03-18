#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""Скрипт собирает вопросы с ru.stackoverflow, связанные с исключениями, но у которых нет метки "исключения"."""


from sqlalchemy import create_engine, Table, Column, Integer, MetaData, DateTime, Boolean
from sqlalchemy.orm import mapper, sessionmaker


class Question:
    def __init__(self, id):
        self.id = id
        self.editable = False
        self.editable_date = None

    def __repr__(self):
        return "<Question(#{}. Editable: {}. Editable_date: {})>".format(self.id, self.editable, self.editable_date)

    def url(self):
        return 'http://ru.stackoverflow.com/questions/' + str(self.id)


def get_session_factory():
    # Создаем базу, включаем логирование и автообновление подключения каждые 2 часа (7200 секунд)
    engine = create_engine(
        # 'sqlite:///:memory:',
        'sqlite:///questions.db',
        # echo=True,
        pool_recycle=7200
    )

    metadata = MetaData()

    comments_table = Table('Question', metadata,
        Column('id', Integer, primary_key=True),
        Column('editable', Boolean),
        Column('editable_date', DateTime)
    )

    mapper(Question, comments_table)
    metadata.create_all(engine)

    return sessionmaker(bind=engine)


Session = get_session_factory()
session = Session()

query = session.query(Question)


from main import get_logger
logger = get_logger('gatherer')


import requests


def search_questions(title, body):
    page = 1

    questions = list()

    while True:
        params = {
            'site': 'ru.stackoverflow',
            'nottagged': 'исключения',

            'title': title,
            'body': body,
            'page': page
        }

        rs = requests.get('https://api.stackexchange.com/2.2/search/advanced', params)
        logger.debug('Rs: %s, rs.url: %s', rs, rs.url)

        rs = rs.json()
        logger.debug('Rs.json: %s', rs)

        for item in rs['items']:
            questions.append(item['question_id'])

        page += 1
        if not rs['has_more']:
            break

        if rs['quota_remaining'] == 0:
            import pickle
            pickle.dump(questions, open('questions_{}'.format(page), 'wb'))

            import time
            time.sleep(60 * 60 * 24 + 3600)

    return questions


if __name__ == '__main__':
    questions = list()
    questions += search_questions('исключения', None)
    questions += search_questions('исключение', None)
    questions += search_questions('exception', None)
    questions += search_questions(None, 'исключения')
    questions += search_questions(None, 'исключение')
    questions += search_questions(None, 'exception')

    for q in set(questions):
        session.add(Question(q))

    session.commit()
