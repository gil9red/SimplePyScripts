#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dis__bytecode__is_empty_function import check_is_empty_function as check_is_empty_function__use_dis
from inspect__get_source__function import check_is_empty_function as check_is_empty_function__use_inspect


def foo():
    pass


def foo2():
    return 1


print("check_is_empty_function__use_inspect:", check_is_empty_function__use_inspect(foo))
print("check_is_empty_function__use_inspect:", check_is_empty_function__use_inspect(foo2))
print()

print("check_is_empty_function__use_dis:", check_is_empty_function__use_dis(foo))
print("check_is_empty_function__use_dis:", check_is_empty_function__use_dis(foo2))
