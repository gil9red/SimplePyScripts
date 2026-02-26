#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from unittest.mock import patch, Mock
import datetime

import _test_datetime


def test() -> None:
    print("local:", datetime.datetime.now(), datetime.datetime.utcnow())
    print("import:", *_test_datetime.get())
    print()


datetime_mock = Mock(wraps=datetime.datetime)
datetime_mock.now.return_value = datetime.datetime(1999, 1, 1)
datetime_mock.utcnow.return_value = datetime.datetime(2000, 1, 1)

test()

with (
    patch("datetime.datetime", new=datetime_mock),
    patch("_test_datetime.datetime", new=datetime_mock)
):
    test()
    # 1999-01-01 00:00:00 2000-01-01 00:00:00

    assert datetime.datetime.now() == datetime.datetime(1999, 1, 1)
    assert datetime.datetime.utcnow() == datetime.datetime(2000, 1, 1)

    now_2, utcnow_2 = _test_datetime.get()
    assert datetime.datetime.now() == now_2
    assert datetime.datetime.utcnow() == utcnow_2

test()
