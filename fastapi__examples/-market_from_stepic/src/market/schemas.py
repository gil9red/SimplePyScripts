#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass, field
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
class CreateShoppingCartModel:
    product_ids: list[str] = field(default_factory=list)


@dataclass
class GetShoppingCartModel(CreateShoppingCartModel, IdBasedObjModel):
    pass


@dataclass
class GetShoppingCartsModel:
    items: list[GetShoppingCartModel]


@dataclass
class LoginModel:
    username: str
    password: str
