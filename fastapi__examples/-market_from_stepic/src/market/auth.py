#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
from typing import Any, Annotated

import jwt
# TODO:
from fastapi import Depends, HTTPException, status
# TODO:
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer

from market import models
from market import services
from market.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


security = HTTPBearer()


# TODO:
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


@dataclass
class TokenPayload:
    sub: str
    role: models.UserRoleEnum
    # TODO: Проверка того, что токен свежий
    exp: datetime | None = None


def create_access_token(
        token: TokenPayload,
        expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
) -> str:
    data: dict[str, Any] = asdict(token)
    data["exp"] = datetime.now(timezone.utc) + expires_delta
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def parse_access_token(token_data: str) -> TokenPayload:
    payload: dict[str, Any] = jwt.decode(token_data, SECRET_KEY, algorithms=[ALGORITHM])
    try:
        return TokenPayload(**payload)
    except Exception:
        raise credentials_exception


# TODO:
# TODO: проверка для разных ролей
# Function to check the user's role based on the bearer token
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> models.User:
    if not credentials:
        raise credentials_exception
    try:
        token = credentials.credentials
        token_data = parse_access_token(token)
        if token_data.role != models.UserRoleEnum.ADMIN:
            raise HTTPException(status_code=403, detail="Not authorized to access this resource")

        # TODO: Проверить, что токен не истек

        # TODO: Проверить, что роль юзера совпадает с тем, что в токене
        user: models.User = services.get_user(token_data.sub)
        if not user:
            raise credentials_exception
        return user

        # return token_data

    except jwt.exceptions.InvalidTokenError:
        raise credentials_exception



if __name__ == "__main__":
    # TODO: в тесты
    token_data = create_access_token(TokenPayload(sub="dfsdfsdfsdfsdf", role=models.UserRoleEnum.ADMIN))
    print(token_data)
    print(parse_access_token(token_data))
