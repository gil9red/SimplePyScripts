# coding=utf-8

__author__ = 'ipetrash'

# EN: Least Common Multiple.
# RU: Наименьшее общее кратное (НОК).

def gcd(a, b):
   "Нахождение НОД"
   while a != 0:
      a,b = b%a,a # параллельное определение
   return b


if __name__ == '__main__':
    a = int(raw_input("a = "))
    b = int(raw_input("b = "))
    print("LCM: %s" % ((a * b) / gcd(a, b)))