#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass
from market.models import UserRole


@dataclass
class IdBasedObjModel:
    id: str


@dataclass
class GetUserModel(IdBasedObjModel):
    role: UserRole
    username: str


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
class CreateProductModel:
    name: str
    price_minor: int  # Копейки
    description: str


@dataclass
class GetShoppingCartModel(IdBasedObjModel):
    products: list[GetProductModel]


@dataclass
class GetShoppingCartsModel:
    items: list[GetShoppingCartModel]


@dataclass
class LoginModel:
    username: str
    password: str
