#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
from typing import Any, Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from market import models
from market import services
from market.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


optional_security = HTTPBearer(auto_error=False)


not_authenticated_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not authenticated",
    headers={"WWW-Authenticate": "Bearer"},
)
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
    exp: datetime | None = None


def create_access_token(
    token: TokenPayload,
    expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
) -> str:
    data: dict[str, Any] = asdict(token)
    data["exp"] = datetime.now(timezone.utc) + expires_delta
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def parse_access_token(token_data: str) -> TokenPayload:
    try:
        payload: dict[str, Any] = jwt.decode(
            token_data, SECRET_KEY, algorithms=[ALGORITHM]
        )
        return TokenPayload(**payload)

    except jwt.exceptions.ExpiredSignatureError:
        raise signature_has_expired_exception

    except Exception:
        raise credentials_exception


def get_current_user_or_none(
    credentials: HTTPAuthorizationCredentials | None = Depends(optional_security),
) -> models.User | None:
    if not credentials:
        return

    token = credentials.credentials
    token_data = parse_access_token(token)

    user: models.User = services.get_user(token_data.sub)
    if not user:
        raise credentials_exception

    # NOTE: Если было понижение в роли? :D
    if token_data.role != user.role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Role in the token and in the database does not match",
        )

    return user


def get_current_user(
    current_user: Annotated[models.User | None, Depends(get_current_user_or_none)],
) -> models.User:
    if not current_user:
        raise not_authenticated_exception

    return current_user


def get_current_user_admin(
    current_user: Annotated[models.User, Depends(get_current_user)],
):
    if current_user.role != models.UserRoleEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Allowed only for admin",
        )
    return current_user


def get_current_user_manager_or_admin(
    current_user: Annotated[models.User, Depends(get_current_user)],
):
    if current_user.role not in [models.UserRoleEnum.MANAGER, models.UserRoleEnum.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Allowed only for admin and manager",
        )
    return current_user


if __name__ == "__main__":
    # TODO: в тесты
    token_data = create_access_token(
        TokenPayload(sub="dfsdfsdfsdfsdf", role=models.UserRoleEnum.ADMIN)
    )
    print(token_data)
    print(parse_access_token(token_data))
