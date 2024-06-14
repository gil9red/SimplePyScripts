#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from fastapi import APIRouter, status
from fastapi.responses import HTMLResponse

from market.schemas import (
    GetUserModel,
    GetUsersModel,
    GetProductModel,
    GetProductsModel,
    CreateProductModel,
    GetShoppingCartModel,
    GetShoppingCartsModel,
    LoginModel,
    CreateProductModel,
)
from market import services


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def index():
    return """\
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
    <div><a href="https://stepik.org/lesson/1186984/step/8?unit=1222202">Урок</a></div>
    <br/>
    <div><a href="/docs">/docs</a></div>
    <div><a href="/redoc">/redoc</a></div>
</body>
</html>
    """


@router.get("/users", response_model=GetUsersModel)
def get_users() -> GetUsersModel:
    return GetUsersModel(
        items=[
            GetUserModel(
                id=user.id,
                role=user.role,
                username=user.username,
            )
            for user in services.get_users()
        ]
    )


@router.get("/products", response_model=GetProductsModel)
def get_products() -> GetProductsModel:
    return GetProductsModel(
        items=[
            GetProductModel(
                id=product.id,
                name=product.name,
                price_minor=product.price_minor,
                description=product.description,
            )
            for product in services.get_products()
        ]
    )


@router.get("/product/{id}", response_model=GetProductModel)
def get_product(id: str) -> GetProductModel:
    obj = services.get_product(id)
    return GetProductModel(
        id=obj.id,
        name=obj.name,
        price_minor=obj.price_minor,
        description=obj.description,
    )


# TODO: Мб в адресе явно указать, что это создание
@router.post(
    "/products",
    response_model=GetProductModel,
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
):
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

    obj = services.create_product(
        name=product.name,
        price_minor=product.price_minor,
        description=product.description,
    )

    return GetProductModel(
        id=obj.id,
        name=obj.name,
        price_minor=obj.price_minor,
        description=obj.description,
    )


@router.get("/shopping-carts", response_model=GetShoppingCartsModel)
def get_shopping_carts() -> GetShoppingCartsModel:
    return GetShoppingCartsModel(
        items=[
            GetShoppingCartModel(
                id=obj.id,
                # user_id=obj.user_id,
                products=[
                    # TODO: Дублирует выше
                    GetProductModel(
                        id=p.id,
                        name=p.name,
                        price_minor=p.price_minor,
                        description=p.description,
                    )
                    for p in obj.products
                ],
            )
            for obj in services.get_shopping_carts()
        ]
    )


@router.get("/shopping-cart/{id}", response_model=GetShoppingCartModel)
def get_shopping_cart(id: str) -> GetShoppingCartModel:
    obj = services.get_shopping_cart(id)

    return GetShoppingCartModel(
        id=obj.id,
        products=[
            # TODO: Дублирует выше
            GetProductModel(
                id=p.id,
                name=p.name,
                price_minor=p.price_minor,
                description=p.description,
            )
            for p in obj.products
        ],
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
