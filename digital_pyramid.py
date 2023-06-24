#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


n = 9

for i in range(1, n + 1):
    left = "".join(map(str, range(1, i)))
    spaces = " " * (n - i)
    print(f"{spaces}{left}{i}{left[::-1]}")

#         1
#        121
#       12321
#      1234321
#     123454321
#    12345654321
#   1234567654321
#  123456787654321
# 12345678987654321

print()

x = ""
for i in range(1, n + 1):
    x += str(i)
    print(" " * (n - i) + x + x[-2::-1])
#         1
#        121
#       12321
#      1234321
#     123454321
#    12345654321
#   1234567654321
#  123456787654321
# 12345678987654321
