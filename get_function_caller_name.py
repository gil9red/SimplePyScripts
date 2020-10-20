#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import inspect


def caller_name() -> str:
    """Return the calling function's name."""
    return inspect.currentframe().f_back.f_code.co_name


if __name__ == '__main__':
    def foo():
        print(caller_name())
        assert caller_name() == 'foo'

    foo()

    def bar():
        def zoo():
            print(caller_name())
            assert caller_name() == 'zoo'
        zoo()

    bar()
