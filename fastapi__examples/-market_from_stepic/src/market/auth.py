#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from market.models import UserRoleEnum


security = HTTPBearer()


@dataclass
class TokenPayload:
    """Base model for the token"""

    sub: str = None
    role: UserRoleEnum = None


# TODO: проверка для разных ролей
# Function to check the user's role based on the bearer token
def check_admin_role(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(status_code=401, detail="Bearer token missing")
    try:
        token = credentials.credentials
        # TODO: замена "secret" на SECRET_KEY
        # TODO: переменная для algorithms
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        token_data = TokenPayload(**payload)
        if token_data.role != UserRoleEnum.ADMIN:
            raise HTTPException(status_code=403, detail="Not authorized to access this resource")
        return token_data
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
