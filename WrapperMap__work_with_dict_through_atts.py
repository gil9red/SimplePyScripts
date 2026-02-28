#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


class WrapperMap:
    def __init__(self, d: dict) -> None:
        self.d = d

    def get_value(self):
        return self.d

    def __getattr__(self, item: str):
        value = self.d.get(item)
        if isinstance(value, dict):
            return self.__class__(value)

        return value

    def __repr__(self) -> str:
        return repr(self.d)


genMessage = {
    "from_user": {
        "id": 123,
        "username": "username",
        "full_name": "fullName",
    },
}
x = WrapperMap(genMessage)

print(x.from_user, type(x.from_user))
# {'id': 123, 'username': 'username', 'full_name': 'fullName'} <class '__main__.WrapperMap'>

print(x.from_user.id, type(x.from_user.id))
# 123 <class 'int'>

print(x.from_user.username, type(x.from_user.username))
# username <class 'str'>
