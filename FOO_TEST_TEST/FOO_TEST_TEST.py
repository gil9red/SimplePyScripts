#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
function underlineText(text) {
    var result = '';

    for (var i = 0, length = text.length; i < length; ++i) {
        result += text.charAt(i)+'\u0332';
    }

    return result;
}
"""

text = ' Вася, HelloWorld! '
underline_text = '\u0332'.join(text)
print(underline_text)
