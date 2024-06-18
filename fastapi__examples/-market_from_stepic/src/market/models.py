#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import enum
from dataclasses import dataclass, field


class UserRoleEnum(enum.StrEnum):
    USER = enum.auto()
    MANAGER = enum.auto()
    ADMIN = enum.auto()


class StatusOrderEnum(enum.StrEnum):
    CREATED = enum.auto()
    IN_PROCESSED = enum.auto()
    FINISHED = enum.auto()
    CANCELED = enum.auto()


@dataclass
class User:
    """Пользователь"""

    id: str
    role: UserRoleEnum
    username: str = None
    hashed_password: str = None


@dataclass
class Product:
    """Товар"""

    id: str
    name: str
    price_minor: int  # Копейки
    description: str


@dataclass
class ShoppingCart:
    """Корзина с товарами"""

    id: str
    name: str = ""
    product_ids: list[str] = field(default_factory=list)


@dataclass
class Order:
    """Заказ"""

    id: str
    email: str
    shopping_cart_id: str
    status: StatusOrderEnum = StatusOrderEnum.CREATED
