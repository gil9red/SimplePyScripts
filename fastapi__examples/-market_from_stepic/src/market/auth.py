#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
# TODO:
from fastapi import Depends, HTTPException, status
# TODO:
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from market.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from market.models import UserRoleEnum


security = HTTPBearer()


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


@dataclass
class TokenPayload:
    sub: str
    role: UserRoleEnum
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
# def check_admin_role(credentials: HTTPAuthorizationCredentials = Depends(security)):
#     if not credentials:
#         raise HTTPException(status_code=401, detail="Bearer token missing")
#     try:
#         token = credentials.credentials
#         token_data = parse_access_token(token)
#         if token_data.role != UserRoleEnum.ADMIN:
#             raise HTTPException(status_code=403, detail="Not authorized to access this resource")
#         return token_data
#     except jwt.exceptions.InvalidTokenError:
#         raise HTTPException(status_code=401, detail="Invalid token")


if __name__ == "__main__":
    # TODO: в тесты
    token_data = create_access_token(TokenPayload(sub="dfsdfsdfsdfsdf", role=UserRoleEnum.ADMIN))
    print(token_data)
    print(parse_access_token(token_data))
