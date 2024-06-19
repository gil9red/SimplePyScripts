#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from typing import Annotated

# TODO:
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from market import db
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
from market import auth


router = APIRouter()


@router.post("/token")
def login_for_access_token(
        # credentials: UserLogin
        credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> LoginResponse:
    if not credentials.username or not credentials.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    user: db.User = services.get_user_by_username(credentials.username)
    if verify_password(credentials.password, user.hashed_password):
        # Generate a JWT token
        access_token = auth.create_access_token(
            token=auth.TokenPayload(user.id, user.role),
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

    raise HTTPException(status_code=400, detail="Incorrect username or password")


@router.get("/users/me/")
def read_users_me(
    # TODO:
    current_user: Annotated[GetUserModel, Depends(auth.get_current_user)],
    # current_user: Annotated[GetUserModel, Depends(auth.get_current_user)],
) -> GetUserModel:
    return current_user


@router.get("/users")
def get_users(
    current_user: Annotated[GetUserModel, Depends(auth.get_current_user)],
) -> GetUsersModel:
    # TODO:
    print(current_user)
    return services.get_users()


@router.get("/user/{id}")
def get_user(id: str) -> GetUserModel:
    return services.get_user(id)


@router.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user: CreateUserModel,
    current_user: Annotated[GetUserModel, Depends(auth.get_current_user)],
) -> IdBasedObjModel:
    # TODO:
    print(current_user)

    return services.create_user(
        role=user.role,
        username=user.username,
        password=user.password,
    )


@router.get("/products")
def get_products() -> GetProductsModel:
    return services.get_products()


@router.get("/product/{id}")
def get_product(id: str) -> GetProductModel:
    return services.get_product(id)


# TODO: Мб в адресе явно указать, что это создание
@router.post(
    "/products",
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


@router.get("/shopping-carts")
def get_shopping_carts() -> GetShoppingCartsModel:
    return services.get_shopping_carts()


@router.get("/shopping-cart/{id}")
def get_shopping_cart(id: str) -> GetShoppingCartModel:
    return services.get_shopping_cart(id)


# TODO: Мб в адресе явно указать, что это создание
@router.post(
    "/shopping-carts",
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


# TODO:
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
