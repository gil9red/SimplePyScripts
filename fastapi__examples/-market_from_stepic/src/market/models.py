#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import enum
from dataclasses import dataclass


class UserRole(enum.StrEnum):
    USER = enum.auto()
    MANAGER = enum.auto()
    ADMIN = enum.auto()


@dataclass
class User:
    """Пользователь"""

    id: str
    role: UserRole
    username: str = None
    password: str = None


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
    product_ids: list[str]


@dataclass
class Order:
    """Заказ"""

    # TODO: Статус заказа - создан, в обработке, завершен, отменен
    id: str
    email: str
    shopping_cart_id: str
