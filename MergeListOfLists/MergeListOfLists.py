__author__ = 'ipetrash'

## EN: Ways to merge a list of lists
## RU: Cпособы слияния списка списков
# source: http://habrahabr.ru/post/63539/
def listmerge1(lstlst):
    all = []
    for lst in lstlst:
        for el in lst:
            all.append(el)
    return all


def listmerge2(lstlst):
    all = []
    for lst in lstlst:
        all = all + lst
    return all


def listmerge3(lstlst):
    all = []
    for lst in lstlst:
        all.extend(lst)
    return all


from functools import reduce

listmerge4a = lambda ll: reduce(lambda a, b: a + b, ll, [])
listmerge4b = lambda ll: sum(ll, [])


listmerge5 = lambda ll: [el for lst in ll for el in lst]


listmerge6a = lambda s: reduce(lambda d, el: d.extend(el) or d, s, [])

import operator
listmerge6b = lambda s: reduce(operator.iadd, s, [])


lstlst = ([6, 6], [1, 2, 3], [4, 5], [6], [7, 8], [9])
print("List: ", lstlst)
print("Result:")
print("1.  ", listmerge1(lstlst))
print("2.  ", listmerge2(lstlst))
print("3.  ", listmerge3(lstlst))
print("4a. ", listmerge4a(lstlst))
print("4b. ", listmerge4b(lstlst))
print("5.  ", listmerge5(lstlst))
print("6a. ", listmerge6a(lstlst))
print("6b. ", listmerge6b(lstlst))