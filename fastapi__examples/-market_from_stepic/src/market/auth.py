#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from market import models
from market import services
from market.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


security = HTTPBearer()


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
signature_has_expired_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Signature has expired",
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
    try:
        payload: dict[str, Any] = jwt.decode(token_data, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenPayload(**payload)

    except jwt.exceptions.ExpiredSignatureError:
        raise signature_has_expired_exception

    except Exception:
        raise credentials_exception


# TODO: проверка для разных ролей
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> models.User:
    if not credentials:
        raise credentials_exception

    token = credentials.credentials
    token_data = parse_access_token(token)

    user: models.User = services.get_user(token_data.sub)
    if not user:
        raise credentials_exception

    # NOTE: Если было понижение в роли? :D
    if token_data.role != user.role:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this resource")

    return user


if __name__ == "__main__":
    # TODO: в тесты
    token_data = create_access_token(TokenPayload(sub="dfsdfsdfsdfsdf", role=models.UserRoleEnum.ADMIN))
    print(token_data)
    print(parse_access_token(token_data))
