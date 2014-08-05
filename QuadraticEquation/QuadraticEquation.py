# coding=utf-8

import argparse
import math

__author__ = 'ipetrash'


def create_parser():
    return argparse.ArgumentParser(description="Finding the roots of a quadratic equation.")


def calculate_D(a, b, c):
    return (b ** 2) - 4 * a * c

	
def calculate_Roots(a, b, D):
    sqrt_D = math.sqrt(D)
    x1 = (-b - sqrt_D) / (2 * a)
    x2 = (-b + sqrt_D) / (2 * a)
    return x1, x2

	
if __name__ == '__main__':
    parse = create_parser()
    parse.parse_args()

    a = int(raw_input("a="))
    b = int(raw_input("b="))
    c = int(raw_input("c="))
    D = calculate_D(a, b, c)
    print("D=%s" % D)
    if D > 0:
        print("Roots x1=%s x2=%s" % (calculate_Roots(a, b, D)))
    elif D is 0:
        print("Root x=%s" % (-b / (2 * a)))
    elif D < 0:
        print("No roots.")