#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import jwt

from fastapi import APIRouter, status, Depends, HTTPException

# TODO:
# from market.auth import check_admin_role, TokenPayload
from market.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from market.security import verify_password
from market.schemas import (
    LoginResponse,
    UserLogin,
    GetUserModel,
    GetUsersModel,
    CreateUserModel,
    GetProductModel,
    GetProductsModel,
    IdBasedObjModel,
    GetShoppingCartModel,
    GetShoppingCartsModel,
    CreateShoppingCartModel,
    CreateProductModel,
)
from market import services


router = APIRouter()


@router.post("/login")
def login(credentials: UserLogin) -> LoginResponse:
    if not credentials.username or not credentials.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # TODO: через services?
    from market.db import db, User
    user: User = db.get_user_by_username(credentials.username)

    if verify_password(credentials.password, user.hashed_password):
        # Generate a JWT token
        access_token = jwt.encode(
            {"sub": credentials.username, "role": user.role},
            SECRET_KEY,
            algorithm=ALGORITHM,
        )

        # Return the access token and user details
        return LoginResponse(
            token=access_token,
            user=GetUserModel(
                id=user.id,
                username=user.username,
                role=user.role,
            ),
        )

    raise HTTPException(status_code=400, detail="Incorrect email or password")


@router.get("/users", response_model=GetUsersModel)
def get_users() -> GetUsersModel:
    return services.get_users()


@router.get("/user/{id}", response_model=GetUserModel)
def get_user(id: str) -> GetUserModel:
    return services.get_user(id)


@router.post(
    "/users",
    response_model=IdBasedObjModel,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user: CreateUserModel,
    # TODO:
    # token_data: TokenPayload = Depends(check_admin_role)
) -> IdBasedObjModel:
    return services.create_user(
        role=user.role,
        username=user.username,
        password=user.password,
    )


@router.get("/products", response_model=GetProductsModel)
def get_products() -> GetProductsModel:
    return services.get_products()


@router.get("/product/{id}", response_model=GetProductModel)
def get_product(id: str) -> GetProductModel:
    return services.get_product(id)


# TODO: Мб в адресе явно указать, что это создание
@router.post(
    "/products",
    response_model=IdBasedObjModel,
    # 201 статус код потому что мы создаем объект – стандарт HTTP
    status_code=status.HTTP_201_CREATED,
    # TODO:
    # # Это нужно для сваггера. Мы перечисляем ответы эндпоинта, чтобы получить четкую документацию.
    # responses={201: {"model": GetArticleModel}, 401: {"model": ErrorModel}, 403: {"model": ErrorModel}},
)
def create_product(
    product: CreateProductModel,
    # TODO:
    # # credentials – тело с логином и паролем. Обычно аутентификация выглядит сложнее, но для нашего случая пойдет и так.
    # credentials: LoginModel,
) -> IdBasedObjModel:
    # TODO:
    # current_user = services.login(
    #     username=credentials.username,
    #     password=credentials.password,
    #     users_repository=MemoryUsersRepository(),
    # )
    #
    # # Это аутентификация
    # if not current_user:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user"
    #     )
    # # а это авторизация
    # if not isinstance(current_user, Admin):
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden resource"
    #     )

    return services.create_product(
        name=product.name,
        price_minor=product.price_minor,
        description=product.description,
    )


@router.get("/shopping-carts", response_model=GetShoppingCartsModel)
def get_shopping_carts() -> GetShoppingCartsModel:
    return services.get_shopping_carts()


@router.get("/shopping-cart/{id}", response_model=GetShoppingCartModel)
def get_shopping_cart(id: str) -> GetShoppingCartModel:
    return services.get_shopping_cart(id)


# TODO: Мб в адресе явно указать, что это создание
@router.post(
    "/shopping-carts",
    response_model=IdBasedObjModel,
    # 201 статус код потому что мы создаем объект – стандарт HTTP
    status_code=status.HTTP_201_CREATED,
    # TODO:
    # # Это нужно для сваггера. Мы перечисляем ответы эндпоинта, чтобы получить четкую документацию.
    # responses={201: {"model": GetArticleModel}, 401: {"model": ErrorModel}, 403: {"model": ErrorModel}},
)
def create_shopping_cart(
    shopping_cart: CreateShoppingCartModel,
    # TODO:
    # # credentials – тело с логином и паролем. Обычно аутентификация выглядит сложнее, но для нашего случая пойдет и так.
    # credentials: LoginModel,
) -> IdBasedObjModel:
    # TODO:
    # current_user = services.login(
    #     username=credentials.username,
    #     password=credentials.password,
    #     users_repository=MemoryUsersRepository(),
    # )
    #
    # # Это аутентификация
    # if not current_user:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user"
    #     )
    # # а это авторизация
    # if not isinstance(current_user, Admin):
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden resource"
    #     )

    return services.create_shopping_cart(
        product_ids=shopping_cart.product_ids,
    )


# @router.post(
#     "/articles",
#     response_model=GetArticleModel,
#     # 201 статус код потому что мы создаем объект – стандарт HTTP
#     status_code=status.HTTP_201_CREATED,
#     # Это нужно для сваггера. Мы перечисляем ответы эндпоинта, чтобы получить четкую документацию.
#     responses={201: {"model": GetArticleModel}, 401: {"model": ErrorModel}, 403: {"model": ErrorModel}},
# )
# def create_article(
#     article: CreateArticleModel,
#     # credentials – тело с логином и паролем. Обычно аутентификация выглядит сложнее, но для нашего случая пойдет и так.
#     credentials: LoginModel,
# ):
#     current_user = services.login(
#         username=credentials.username,
#         password=credentials.password,
#         users_repository=MemoryUsersRepository(),
#     )
#
#     # Это аутентификация
#     if not current_user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user"
#         )
#     # а это авторизация
#     if not isinstance(current_user, Admin):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden resource"
#         )
#
#     article = services.create_article(
#         title=article.title,
#         content=article.content,
#         articles_repository=ShelveArticlesRepository(),
#     )
#
#     return GetArticleModel(id=article.id, title=article.title, content=article.content)
