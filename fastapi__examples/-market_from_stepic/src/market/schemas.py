#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pydantic import BaseModel
from market.models import UserRole


class GetUserModel(BaseModel):
    id: str
    role: UserRole
    username: str


class GetUsersModel(BaseModel):
    items: list[GetUserModel]


# TODO: Product из models.py
class GetProductModel(BaseModel):
    id: str
    name: str
    price_minor: int  # Копейки
    description: str


class GetProductsModel(BaseModel):
    items: list[GetProductModel]


class CreateProductModel(BaseModel):
    name: str
    price_minor: int  # Копейки
    description: str


class GetShoppingCartModel(BaseModel):
    id: str
    user_id: str
    products: list[GetProductModel]


class GetShoppingCartsModel(BaseModel):
    items: list[GetShoppingCartModel]


class LoginModel(BaseModel):
    username: str
    password: str


class ErrorModel(BaseModel):
    detail: str
