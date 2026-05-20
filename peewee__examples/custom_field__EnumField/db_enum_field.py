#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import enum
from typing import Type, Any

from peewee import CharField


class EnumField(CharField):
    """
    This class enable an Enum like field for Peewee
    """

    def __init__(self, choices: Type[enum.Enum], *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.choices: Type[enum.Enum] = choices
        self.max_length: int = 255

    def db_value(self, value: Any) -> Any:
        if value is None:
            return

        if isinstance(value, enum.Enum):
            return value.value

        return value

    def python_value(self, value: Any) -> Any:
        if value is None:
            return

        type_value_enum = type(list(self.choices)[0].value)
        value_enum = type_value_enum(value)
        return self.choices(value_enum)
