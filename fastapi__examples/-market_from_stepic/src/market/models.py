#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import enum
from dataclasses import dataclass, field, fields
from typing import Any


# TODO: аннотации
def create_from(cls, other):
    data: dict[str, Any] = dict.fromkeys(
        f.name for f in fields(cls)
    )
    for f in fields(other):
        name = f.name
        if name in data:
            data[name] = getattr(other, name)

    return cls(**data)


class UserRoleEnum(enum.StrEnum):
    MANAGER = enum.auto()
    ADMIN = enum.auto()


class StatusOrderEnum(enum.StrEnum):
    CREATED = enum.auto()
    IN_PROCESSED = enum.auto()
    FINISHED = enum.auto()
    CANCELED = enum.auto()


@dataclass
class IdBasedObj:
    id: str


@dataclass
class User(IdBasedObj):
    role: UserRoleEnum
    username: str = None


@dataclass
class UserInDb(User):
    hashed_password: str = None


@dataclass
class LoginResponse:
    token: str
    user: User


@dataclass
class CreateUser:
    username: str
    password: str
    role: UserRoleEnum


@dataclass
class Users:
    items: list[User]


@dataclass
class CreateProduct:
    """Товар"""

    name: str
    price_minor: int  # Копейки
    description: str


@dataclass
class Product(CreateProduct, IdBasedObj):
    pass


@dataclass
class Product(IdBasedObj):
    """Товар"""

    name: str
    price_minor: int  # Копейки
    description: str


@dataclass
class Products:
    items: list[Product]


@dataclass
class CreateShoppingCart:
    """Корзина с товарами"""

    name: str = ""
    product_ids: list[str] = field(default_factory=list)


@dataclass
class ShoppingCart(CreateShoppingCart, IdBasedObj):
    """Корзина с товарами"""


@dataclass
class ShoppingCarts:
    items: list[ShoppingCart]


class CreateOrder:
    """Заказ"""

    email: str
    shopping_cart_id: str
    status: StatusOrderEnum = StatusOrderEnum.CREATED


@dataclass
class Order(CreateOrder, IdBasedObj):
    """Заказ"""


# TODO: в тесты
# user1 = UserInDb("123", UserRoleEnum.ADMIN, "dfsf", "dddd")
# print(user1)
# user2 = User("123", UserRoleEnum.ADMIN, "dfsf")
# print(user2)
# # print(User(**user1))
# print()
#
# print(*fields(user1), sep="\n")
# print(fields(User))
#
# print(create_from(User, user1))
