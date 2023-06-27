#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os

from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


Base = declarative_base()


class Serial(Base):
    """
    Класс описывает таблицу Serial.

    """

    __tablename__ = "Serial"

    Id = Column(Integer, primary_key=True)
    OriginalName = Column(String)
    EnglishName = Column(String)
    RussianName = Column(String)

    # Список жанров, разделенных ; (точка с запятой)
    Genre = Column(String)
    ReleaseDate = Column(String)
    Producer = Column(String)
    AuthorOriginal = Column(String)
    Annotation = Column(String)

    Cover = Column(String)
    Screenshots = Column(String)

    # Количество серий сериала
    Count = Column(Integer)

    # Поле, ссылкающееся на SerialVideo, которое содержит список объектов SerialVideo, с которыми
    # связан текущий объек. Также создает в SerialVideo поле Serial, которое указывает на текущий объект
    # TODO: для удаления связанных сериалов: http://docs.sqlalchemy.org/en/latest/orm/cascades.html#unitofwork-cascades
    Videos = relationship("SerialVideo", backref="Serial", order_by="SerialVideo.Id")

    def __repr__(self):
        return f'<Serial(EnglishName: "{self.EnglishName}", Count: {len(self.Videos)})>'


class SerialVideo(Base):
    """
    Класс описывает таблицу SerialVideo.

    """

    __tablename__ = "SerialVideo"

    Id = Column(Integer, primary_key=True)
    SerialId = Column(Integer, ForeignKey("Serial.Id"))

    FileName = Column(String)
    Number = Column(Integer)
    Title = Column(String)
    Duration = Column(Integer)

    def __repr__(self):
        return f'<Serial(Number: "{self.Number}", Serial: {self.Serial.EnglishName})>'


if __name__ == "__main__":
    # http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html
    # http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html
    # http://lectureswww.readthedocs.io/6.www.sync/2.codding/9.databases/2.sqlalchemy/3.orm.html
    # https://bitbucket.org/zzzeek/pycon2013_student_package/src/a5b84d0659cbf1df11766fbbdc215dbe32be8044/04_orm.py?at=master&fileviewer=file-view-default#cl-313
    # http://docs.sqlalchemy.org/en/latest/orm/cascades.html#unitofwork-cascades

    # DEBUG = True
    DEBUG = False

    DIR = os.path.dirname(__file__)
    # engine = sqlalchemy.create_engine('sqlite:///' + os.path.join(DIR, 'database'), echo=True)
    engine = create_engine("sqlite:///:memory:", echo=DEBUG)

    # Создание базы если ее нет
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    serial = Serial(
        OriginalName="Vasya",
        EnglishName="Vasya",
        RussianName="Вася",
        Genre="триллер;боевик",
    )
    serial.Videos.append(SerialVideo(Number="1", FileName="1.avi"))
    serial.Videos.append(SerialVideo(Number="2", FileName="2.avi"))
    serial.Videos.append(SerialVideo(Number="3", FileName="3.avi"))

    session.add(serial)

    session.commit()

    print()
    for _ in session.query(Serial).all():
        print(_)

    print()
    for _ in session.query(SerialVideo).all():
        print(_)
