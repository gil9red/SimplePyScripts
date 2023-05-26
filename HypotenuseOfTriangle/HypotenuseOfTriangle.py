# coding=utf-8


__author__ = "ipetrash"


import argparse
import math


def createParser():
    parse = argparse.ArgumentParser(
        description="Программа высчитывает гипотенузу прямоугольного треугольника"
    )
    parse.add_argument("-a", type=int, help="Первый катет")
    parse.add_argument("-b", type=int, help="второй катет")
    return parse


def hypotenuse(a, b):
    """
    Функция высчитывает гипотенузу прямоугольного треугольника.
    :param a: Первый катет
    :param b: Второй катет
    :return: Гипотенуза
    """
    return math.sqrt(a**2 + b**2)


if __name__ == "__main__":
    parse = createParser()
    args = parse.parse_args()
    if args.a is not None and args.b is not None:
        a = args.a
        b = args.b
        print(f"Катет а={a}, катет b={b}, гипотенуза с={hypotenuse(a, b)}")
    else:
        a = int(input("Введи катет a: "))
        b = int(input("Введи катет b: "))
        print(f"Гипотенуза с={hypotenuse(a, b)}")
