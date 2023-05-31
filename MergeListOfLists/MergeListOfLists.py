__author__ = "ipetrash"


# EN: Ways to merge a list of lists
# RU: Cпособы слияния списка списков


import operator
from functools import reduce


# Source: http://habrahabr.ru/post/63539/
def list_merge_1(lstlst):
    all = []
    for lst in lstlst:
        for el in lst:
            all.append(el)
    return all


def list_merge_2(lstlst):
    all = []
    for lst in lstlst:
        all = all + lst
    return all


def list_merge_3(lstlst):
    all = []
    for lst in lstlst:
        all.extend(lst)
    return all


list_merge_4_a = lambda ll: reduce(lambda a, b: a + b, ll, [])
list_merge_4_b = lambda ll: sum(ll, [])

list_merge_5 = lambda ll: [el for lst in ll for el in lst]

list_merge_6_a = lambda s: reduce(lambda d, el: d.extend(el) or d, s, [])
list_merge_6_b = lambda s: reduce(operator.iadd, s, [])


lst_lst = ([6, 6], [1, 2, 3], [4, 5], [6], [7, 8], [9])
print("List: ", lst_lst)
print("Result:")
print("1.  ", list_merge_1(lst_lst))
print("2.  ", list_merge_2(lst_lst))
print("3.  ", list_merge_3(lst_lst))
print("4a. ", list_merge_4_a(lst_lst))
print("4b. ", list_merge_4_b(lst_lst))
print("5.  ", list_merge_5(lst_lst))
print("6a. ", list_merge_6_a(lst_lst))
print("6b. ", list_merge_6_b(lst_lst))
