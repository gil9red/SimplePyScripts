#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


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


if __name__ == "__main__":
    import json

    class_list = input()

    class_list = json.loads(class_list)

    class Class:
        def __init__(self, name) -> None:
            self.name = name
            self.children = list()

        def all_children(self, children=None):
            if not children:
                children = list()

            for sub_cls in self.children:
                children.append(sub_cls)
                sub_cls.all_children(children)

            return children

        def __str__(self) -> str:
            return f'<Class "{self.name}": {[cls.name for cls in self.children]}>'

        def __repr__(self) -> str:
            return self.__str__()

    dict_class_by_name_dict = {cls["name"]: cls for cls in class_list}

    # Сначала создаем объекты всех классов и заполняем их в словаре
    class_by_name_dict = {name: Class(name) for name in dict_class_by_name_dict}

    # После создания всех объектов, перебираем, получаем их родителей, которые
    # из свежесозданного словаря получаем, чтобы у их родителей заполнить список детей
    for name, dict_cls in dict_class_by_name_dict.items():
        cls = class_by_name_dict[name]

        for parent_cls_name in dict_cls["parents"]:
            parent_cls = class_by_name_dict[parent_cls_name]
            parent_cls.children.append(cls)

    # Сортировка по имени класса
    for name, cls in sorted(class_by_name_dict.items(), key=lambda x: x[0]):
        # Получение списка имен детей, из которого удаляются повторы (с помощью множества) и подсчет
        # количества элементов. По условию, класс является потомком самого себя, поэтому прибавляем 1
        number = len(set(child_cls.name for child_cls in cls.all_children()))
        print(f"{name} : {number + 1}")
