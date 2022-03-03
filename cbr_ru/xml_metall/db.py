#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT
import enum
import time

from decimal import Decimal
from typing import Type, Optional, List, Iterable, Any

# pip install peewee
from peewee import (
    Model, TextField, ForeignKeyField, CharField, DecimalField, DateField, Field
)
from playhouse.sqliteq import SqliteQueueDatabase

import parser

from config import DB_FILE_NAME, ITEMS_PER_PAGE, START_DATE
from parser import MetalEnum


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/cd5bf42742b2de4706a82aecb00e20ca0f043f8e/shorten.py
def shorten(text: str, length=30) -> str:
    if not text:
        return text

    if len(text) > length:
        text = text[:length] + '...'

    return text


class EnumField(CharField):
    """
    This class enable an Enum like field for Peewee
    """

    def __init__(self, choices: Type[enum.Enum], *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.choices: Type[enum.Enum] = choices
        self.max_length = 255

    def db_value(self, value: Any) -> Any:
        return value.value

    def python_value(self, value: Any) -> Any:
        type_value_enum = type(list(self.choices)[0].value)
        value_enum = type_value_enum(value)
        return self.choices(value_enum)


# This working with multithreading
# SOURCE: http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#sqliteq
db = SqliteQueueDatabase(
    DB_FILE_NAME,
    pragmas={
        'foreign_keys': 1,
        'journal_mode': 'wal',    # WAL-mode
        'cache_size': -1024 * 64  # 64MB page-cache
    },
    use_gevent=False,     # Use the standard library "threading" module.
    autostart=True,
    queue_max_size=64,    # Max. # of pending writes that can accumulate.
    results_timeout=5.0   # Max. time to wait for query to be executed.
)


class BaseModel(Model):
    """
    Базовая модель для классов-таблиц
    """

    class Meta:
        database = db

    def get_new(self) -> Type['BaseModel']:
        return type(self).get(self._pk_expr())

    @classmethod
    def get_first(cls) -> Type['BaseModel']:
        return cls.select().first()

    @classmethod
    def get_last(cls) -> Type['BaseModel']:
        return cls.select().order_by(cls.id.desc()).first()

    @classmethod
    def paginating(
            cls,
            page: int = 1,
            items_per_page: int = ITEMS_PER_PAGE,
            order_by: Field = None,
            filters: Iterable = None,
    ) -> List[Type['BaseModel']]:
        query = cls.select()

        if filters:
            query = query.filter(*filters)

        if order_by:
            query = query.order_by(order_by)

        query = query.paginate(page, items_per_page)
        return list(query)

    @classmethod
    def get_inherited_models(cls) -> List[Type['BaseModel']]:
        return sorted(cls.__subclasses__(), key=lambda x: x.__name__)

    @classmethod
    def count(cls) -> int:
        return cls.select().count()

    @classmethod
    def print_count_of_tables(cls):
        items = []
        for sub_cls in cls.get_inherited_models():
            name = sub_cls.__name__
            count = sub_cls.count()
            items.append(f'{name}: {count}')

        print(', '.join(items))

    def __str__(self):
        fields = []
        for k, field in self._meta.fields.items():
            v = getattr(self, k)

            if isinstance(field, (TextField, CharField)):
                if v:
                    if isinstance(v, enum.Enum):
                        v = v.value

                    v = repr(shorten(v))

            elif isinstance(field, ForeignKeyField):
                k = f'{k}_id'
                if v:
                    v = v.id

            fields.append(f'{k}={v}')

        return self.__class__.__name__ + '(' + ', '.join(fields) + ')'


class MetalRate(BaseModel):
    date = DateField()
    metal = EnumField(choices=MetalEnum)
    amount = DecimalField(decimal_places=2)

    class Meta:
        indexes = (
            (('date', 'metal'), True),
        )

    @classmethod
    def get_by(cls, date: DT.date, metal: MetalEnum) -> Optional['MetalRate']:
        return cls.get_or_none(date=date, metal=metal)

    @classmethod
    def add(cls, date: DT.date, metal: MetalEnum, amount: Decimal) -> 'MetalRate':
        obj = cls.get_by(date, metal)
        if not obj:
            obj = cls.create(
                date=date,
                metal=metal,
                amount=amount,
            )

        return obj

    @classmethod
    def add_from(cls, metal_rate: parser.MetalRate) -> 'MetalRate':
        return cls.add(metal_rate.date, metal_rate.metal, metal_rate.amount)

    @classmethod
    def get_last_date(cls) -> DT.date:
        return cls.get_last_dates(number=1)[0]

    @classmethod
    def get_last_dates(cls, number: int) -> list[DT.date]:
        query = cls.select(cls.date).distinct().limit(number).order_by(cls.date.desc())
        items = [rate.date for rate in query]
        if not items:
            items.append(START_DATE)
        return items

    @classmethod
    def get_last_rates_as_dict(cls, number: int) -> dict[DT.date, dict[MetalEnum, Decimal]]:
        date_by_rates = dict()

        dates = cls.get_last_dates(number)
        query = cls.select().where(cls.date.in_(dates)).order_by(cls.date.asc(), cls.metal.asc())
        for rate in query:
            if rate.date not in date_by_rates:
                date_by_rates[rate.date] = dict()

            date_by_rates[rate.date][rate.metal] = rate.amount

        return date_by_rates


db.connect()
db.create_tables(BaseModel.get_inherited_models())

# Задержка в 50мс, чтобы дать время на запуск SqliteQueueDatabase и создание таблиц
# Т.к. в SqliteQueueDatabase запросы на чтение выполняются сразу, а на запись попадают в очередь
time.sleep(0.050)

if __name__ == '__main__':
    BaseModel.print_count_of_tables()
    # MetalRate: 21830
    print()

    print('Last date:', MetalRate.get_last_date())
    # Last date: 2022-03-03

    dates = MetalRate.get_last_dates(number=7)
    print('Last 7 dates:', [str(d) for d in dates])
    # Last 7 dates: ['2022-03-03', '2022-03-02', '2022-03-01', '2022-02-26', '2022-02-25', '2022-02-23', '2022-02-22']

    print()

    date_by_rates = MetalRate.get_last_rates_as_dict(number=3)
    for date, metal_by_amount in date_by_rates.items():
        print(f'{date}:')

        for metal, amount in metal_by_amount.items():
            print(f'    {metal.name}: {amount}')

        print()
    """
    2022-03-01:
        Gold: 5725.1
        Palladium: 7492.89
        Platinum: 3197.49
        Silver: 72.82
    
    2022-03-02:
        Gold: 5664.73
        Palladium: 7565.96
        Platinum: 3123.72
        Silver: 71.82
    
    2022-03-03:
        Gold: 6393.4
        Palladium: 8800.05
        Platinum: 3531.97
        Silver: 81.79
    """
