#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def get_attribute_value_by_local_name(node, attr_name: str) -> str | None:
    for name, value in node.attrs.items():
        # Получаем имя атрибута
        name = name.split(":")[-1]
        if name == attr_name:
            return value

    return
