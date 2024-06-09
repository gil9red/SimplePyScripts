#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass


@dataclass
class User:
    """Обычный пользователь"""

    id: str


@dataclass
class Manager(User):
    """Пользователь, наделенный правами менеджера"""

    username: str
    password: str


@dataclass
class Admin(Manager):
    """Пользователь, наделенный правами администратора"""


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
    user_id: str
    products: list[Product]
