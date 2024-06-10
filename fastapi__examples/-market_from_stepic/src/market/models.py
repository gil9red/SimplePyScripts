#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import enum

# TODO: Мб использовать pydantic? Разве это не про одно и тоже в schemas.py
from dataclasses import dataclass


class UserRole(enum.StrEnum):
    USER = enum.auto()
    MANAGER = enum.auto()
    ADMIN = enum.auto()


@dataclass
class User:
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
    user_id: str
    products: list[Product]
