#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def pretty_money_format(money):
    money = str(money)

    import re
    money = re.sub('[^\\.,\\d]', '', money)

    if (money.count('.') + money.count(',')) > 1:
        raise Exception('Invalid money format: {}.'.format(money))

    money_sep = None
    if money.count('.'):
        money_sep = '.'
    elif money.count(','):
        money_sep = ','

    if money_sep is not None:
        major, minor = money.split(money_sep)
    else:
        major = money

    if len(major) > 3:
        major = list(reversed(major))

        new_major = list()

        i = 0
        for c in major:
            i += 1

            new_major.append(c)
            if i > 0 and i % 3 == 0:
                new_major.append(" ")

        major = ''.join(reversed(new_major))

    money = major
    if money_sep is not None:
        money = major + money_sep + minor

    return money.strip()


if __name__ == '__main__':
    assert pretty_money_format(1000) == '1 000'
    assert pretty_money_format(1000000) == '1 000 000'
    assert pretty_money_format(10000.56) == '10 000.56'
    assert pretty_money_format(1000000.0) == '1 000 000.0'
    assert pretty_money_format(100000) == '100 000'

    assert pretty_money_format('1000') == '1 000'
    assert pretty_money_format('1000000') == '1 000 000'
    assert pretty_money_format('10000.50') == '10 000.50'
    assert pretty_money_format('1000000.0') == '1 000 000.0'
    assert pretty_money_format('100000') == '100 000'

    assert pretty_money_format('10 00') == '1 000'
    assert pretty_money_format('100 00 00') == '1 000 000'
    assert pretty_money_format('1 0000.50$') == '10 000.50'
    assert pretty_money_format('100 00 00.0') == '1 000 000.0'
    assert pretty_money_format('100!000#') == '100 000'
