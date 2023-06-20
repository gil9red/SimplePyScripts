#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/zopefoundation/roman


import roman


print(roman.toRoman(5))  # V
print(roman.toRoman(9))  # IX
print(roman.toRoman(10))  # X
print(roman.toRoman(13))  # XIII
print(roman.toRoman(255))  # CCLV
print(roman.toRoman(1024))  # MXXIV
print()

print(roman.fromRoman("V"))  # 5
print(roman.fromRoman("IX"))  # 9
print(roman.fromRoman("X"))  # 10
print(roman.fromRoman("XIII"))  # 13
print(roman.fromRoman("CCLV"))  # 255
print(roman.fromRoman("MXXIV"))  # 1024

assert roman.fromRoman(roman.toRoman(5)) == 5
assert roman.fromRoman(roman.toRoman(1024)) == 1024
assert roman.fromRoman(roman.toRoman(4048)) == 4048

assert roman.toRoman(roman.fromRoman("MXXIV")) == "MXXIV"
assert roman.toRoman(roman.fromRoman("XIII")) == "XIII"
assert roman.toRoman(roman.fromRoman("IX")) == "IX"
