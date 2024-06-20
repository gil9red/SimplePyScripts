#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import enum
from dataclasses import dataclass, field


class UserRoleEnum(enum.StrEnum):
    # TODO:
    # USER = enum.auto()
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


@dataclass
class IdBasedObjModel:
    id: str


@dataclass
class GetUserModel(IdBasedObjModel):
    role: UserRoleEnum
    username: str


@dataclass
class LoginResponse:
    token: str
    user: GetUserModel


@dataclass
class UserLogin:
    username: str
    password: str


@dataclass
class CreateUserModel(UserLogin):
    role: UserRoleEnum
    username: str
    password: str


@dataclass
class GetUsersModel:
    items: list[GetUserModel]


@dataclass
class CreateProductModel:
    name: str
    price_minor: int  # Копейки
    description: str


@dataclass
class GetProductModel(CreateProductModel, IdBasedObjModel):
    pass


@dataclass
class GetProductsModel:
    items: list[GetProductModel]


@dataclass
class CreateShoppingCartModel:
    name: str = ""
    product_ids: list[str] = field(default_factory=list)


@dataclass
class GetShoppingCartModel(CreateShoppingCartModel, IdBasedObjModel):
    pass


@dataclass
class GetShoppingCartsModel:
    items: list[GetShoppingCartModel]
