#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass
# from pydantic import BaseModel
from market.models import UserRole


@dataclass
# class GetUserModel(BaseModel):
class GetUserModel:
    id: str
    role: UserRole
    username: str


@dataclass
class GetUsersModel:
# class GetUsersModel(BaseModel):
    items: list[GetUserModel]


@dataclass
class GetProductModel:
# TODO: Product из models.py
# class GetProductModel(BaseModel):
    id: str
    name: str
    price_minor: int  # Копейки
    description: str


@dataclass
# class GetProductsModel(BaseModel):
class GetProductsModel:
    items: list[GetProductModel]


@dataclass
class CreateProductModel:
# class CreateProductModel(BaseModel):
    name: str
    price_minor: int  # Копейки
    description: str


@dataclass
class GetShoppingCartModel:
# class GetShoppingCartModel(BaseModel):
    id: str
    # user_id: str
    products: list[GetProductModel]


@dataclass
class GetShoppingCartsModel:
# class GetShoppingCartsModel(BaseModel):
    items: list[GetShoppingCartModel]


@dataclass
class LoginModel:
# class LoginModel(BaseModel):
    username: str
    password: str


@dataclass
class ErrorModel:
# class ErrorModel(BaseModel):
    detail: str
