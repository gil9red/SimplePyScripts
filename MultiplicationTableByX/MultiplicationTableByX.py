# coding=utf-8
# Реализовать функцию-генератор строки с таблицей умножения на число Х.

__author__ = 'ipetrash'

if __name__ == '__main__':
    x = int(raw_input("Input x: "))
    print(' '.join(['%d' % (i * x) for i in xrange(1, 10 + 1)]))