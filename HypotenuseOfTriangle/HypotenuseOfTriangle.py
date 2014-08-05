# coding=utf-8
import math
import argparse

__author__ = 'ipetrash'

def createParser():
    parse = argparse.ArgumentParser(description=u"Программа высчитывает гипотенузу прямоугольного треугольника")
    parse.add_argument("-a", type=int, help=u"Первый катет")
    parse.add_argument("-b", type=int, help=u"второй катет")
    return parse


def hypotenuse(a, b):
    u"""
    Функция высчитывает гипотенузу прямоугольного треугольника.
    :param a: Первый катет
    :param b: Второй катет
    :return: Гипотенуза
    """
    return math.sqrt(a ** 2 + b ** 2)


if __name__ == '__main__':
    parse = createParser()
    args = parse.parse_args()
    if args.a is not None and args.b is not None:
        a = args.a
        b = args.b
        print(u"Катет а=%s, катет b=%s, гипотенуза с=%s" % (a, b, hypotenuse(a, b)))
    else:
        a = int(raw_input(u"Введи катет a: "))
        b = int(raw_input(u"Введи катет b: "))
        print(u"Гипотенуза с=%s" % hypotenuse(a, b))