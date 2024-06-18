#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass, field
from market.models import UserRoleEnum


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
