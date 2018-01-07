#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def check_is_empty_function(function):
    import inspect
    lines = inspect.getsourcelines(function)
    return lines[0][-1].strip() == 'pass'


if __name__ == '__main__':
    def foo():
        pass

    def foo2():
        return 1

    print('Empty:', check_is_empty_function(foo))
    print('Empty:', check_is_empty_function(foo2))
