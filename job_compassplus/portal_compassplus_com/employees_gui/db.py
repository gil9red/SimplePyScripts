#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import base64
import os

from urllib.parse import urljoin

from lxml import etree

from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import config


# TODO: добавить модуль logging


Base = declarative_base()


class Employee(Base):
    """
    Класс описывает сотрудника.

    """

    __tablename__ = "Employees"

    id = Column(String, primary_key=True)
    url = Column(String)
    name = Column(String)
    short_name = Column(String)
    birthday = Column(String)
    job = Column(String)
    department = Column(String)
    photo = Column(String)
    work_phone = Column(String)
    mobile_phone = Column(String)
    email = Column(String)

    @staticmethod
    def parse(xml, session):
        """Функция парсит строку xml с информацией о сотруднике и возвращает заполненный объект Employee."""

        root = etree.HTML(xml)

        employee = Employee()

        # Если одно из них не будет определено, прекратить парсинг
        try:
            employee.id = root.xpath('//node()[@class="lookup-item"]/@id')[0].replace(
                "user-", ""
            )
            employee.short_name = root.xpath('//node()[@class="lookup-item"]/@value')[0]
            employee.name = root.xpath('//node()[@class="lookup-item"]/@name')[0]
            employee.url = root.xpath('//node()[@class="employee-name"]//a/@href')[0]
        except IndexError as e:
            print("error", "employee.id/short_name/name/url", e)
            raise Exception("Bad parsing!")

        try:
            # Загрузка страницы пользователя и вытаскивание дня его рождения
            rs = session.get(employee.url)
            user_root = etree.HTML(rs.text)
            rs = user_root.xpath(
                '//node()[contains(@id, "Birthday")]'
                '/node()[@class="ms-tableCell ms-profile-detailsValue"]/text()'
            )
            employee.birthday = rs[0]
        except Exception as e:
            print("error", "employee.birthday", e, employee.url)
            employee.birthday = ""

        try:
            photo_url = root.xpath('//node()[@class="employee-photo"]/img/@src')[0]

            # Относительный адрес делаем абсолютным
            if photo_url.startswith("/"):
                photo_url = urljoin(config.URL, photo_url)

            rs = session.get(photo_url)
            if rs.ok:
                employee.photo = base64.b64encode(rs.content).decode()

        except Exception as e:
            print("warn", "employee.photo", e)
            employee.photo = ""

        try:
            employee.job = root.xpath(
                '//node()[@class="employee-jobtitle"]/span[2]/text()'
            )[0].strip()
        except IndexError as e:
            print("warn", "employee.job", e)
            employee.job = ""

        try:
            employee.department = root.xpath(
                '//node()[@class="employee-department"]/span[2]/text()'
            )[0].strip()
        except IndexError as e:
            print("warn", "employee.department", e)
            employee.department = ""

        try:
            employee.work_phone = ""
            employee.mobile_phone = ""

            for div_phone in root.xpath('//node()[@class="employee-workphone"]'):
                title, text = [el.text.strip() for el in div_phone.getchildren()]
                if "Work" in title:
                    employee.work_phone = text

                elif "Mobile" in title:
                    employee.mobile_phone = text

        except Exception as e:
            print("warn", "employee.work_phone/mobile_phone", e)
            pass

        try:
            employee.email = root.xpath(
                '//node()[@class="employee-email"]/a/span/text()'
            )[0].strip()
        except IndexError as e:
            print("warn", "employee.email", e)
            employee.email = ""

        return employee

    def __str__(self) -> str:
        return f'<Employee("{self.name}" ({self.short_name}), job: {self.job}, department: {self.department})>'

    def __repr__(self) -> str:
        return self.__str__()


def get_session():
    DIR = os.path.dirname(__file__)
    DB_FILE_NAME = "sqlite:///" + os.path.join(DIR, "database")
    # DB_FILE_NAME = 'sqlite:///:memory:'

    # Создаем базу, включаем логирование и автообновление подключения каждые 2 часа (7200 секунд)
    engine = create_engine(
        DB_FILE_NAME,
        # echo=True,
        pool_recycle=7200,
    )

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    return Session()


db_session = get_session()


def exists(employee_id) -> bool:
    return (
        db_session.query(Employee).filter(Employee.id == employee_id).scalar()
        is not None
    )
