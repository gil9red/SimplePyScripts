#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import re
from seconds_to_str import seconds_to_str


PATTERN_TIME = re.compile(r'(\d\d:\d\d:\d\d)')
PATTERN_EXPR_WITH_TIME = re.compile(f'^{PATTERN_TIME.pattern}(?: [+-] {PATTERN_TIME.pattern})*$')


def get_seconds(hh_mm_ss: str) -> int:
    hh, mm, ss = map(int, hh_mm_ss.split(':'))
    return hh * 3600 + mm * 60 + ss


def preprocess_expr_with_time(text: str) -> str:
    return PATTERN_TIME.sub(lambda m: str(get_seconds(m[1])), text)


def eval_expr_with_time(text: str) -> str:
    if not PATTERN_EXPR_WITH_TIME.match(text):
        raise Exception(f'Expression {text!r} not valid!')

    text = preprocess_expr_with_time(text)
    total_seconds = eval(text)
    return seconds_to_str(total_seconds)


if __name__ == '__main__':
    text = '08:53:11 - 07:15:00 + 08:56:12'

    print(eval_expr_with_time(text))
    # 10:34:23

    assert get_seconds('00:00:01') == 1
    assert get_seconds('00:01:01') == 61
    assert get_seconds('01:01:01') == 3661

    assert preprocess_expr_with_time('00:00:01') == '1'
    assert preprocess_expr_with_time('00:00:01 + 00:01:01 + 01:01:01') == '1 + 61 + 3661'

    assert eval_expr_with_time('08:53:11') == '08:53:11'
    assert eval_expr_with_time('00:00:01 + 00:01:01 + 01:01:01') == '01:02:03'
