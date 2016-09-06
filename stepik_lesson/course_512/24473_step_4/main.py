#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Вам дано описание наследования классов в формате JSON.
Описание представляет из себя массив JSON-объектов, которые соответствуют классам. У каждого JSON-объекта есть поле
name, которое содержит имя класса, и поле parents, которое содержит список имен прямых предков.

Пример:
[{"name": "A", "parents": []}, {"name": "B", "parents": ["A", "C"]}, {"name": "C", "parents": ["A"]}]

Эквивалент на Python:
class A:
    pass

class B(A, C):
    pass

class C(A):
    pass

Гарантируется, что никакой класс не наследуется от себя явно или косвенно, и что никакой класс не наследуется явно
от одного класса более одного раза.
Для каждого класса вычислите предком скольких классов он является и выведите эту информацию в следующем формате.
<имя класса> : <количество потомков>
Выводить классы следует в лексикографическом порядке.

Sample Input:
[{"name": "A", "parents": []}, {"name": "B", "parents": ["A", "C"]}, {"name": "C", "parents": ["A"]}]

Sample Output:
A : 3
B : 1
C : 2

"""


if __name__ == '__main__':
    class_list = input()
    # class_list = '[{"name": "A", "parents": []}, {"name": "B", "parents": ["A", "C"]}, {"name": "C", "parents": ["A"]}]'

    import json
    class_list = json.loads(class_list)

    from collections import defaultdict
    cls_parent_count_dict = defaultdict(int)

    for cls in class_list:
        # По заданию, класс является предком самого себя
        cls_parent_count_dict[cls['name']] += 1

        for cls2 in class_list:
            # Не смысла у самого себя проверять
            if cls == cls2:
                continue

            if cls['name'] in cls2['parents']:
                cls_parent_count_dict[cls['name']] += 1

    # Сортировка по имени класса
    for k in sorted(cls_parent_count_dict.keys()):
        print('{} : {}'.format(k, cls_parent_count_dict[k]))
