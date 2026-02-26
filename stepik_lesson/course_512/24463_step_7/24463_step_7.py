#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Вам дано описание наследования классов исключений в следующем формате.
<имя исключения 1> : <имя исключения 2> <имя исключения 3> ... <имя исключения k>
Это означает, что исключение 1 наследуется от исключения 2, исключения 3, и т. д.

Или эквивалентно записи:

class Error1(Error2, Error3 ... ErrorK):
    pass


Антон написал код, который выглядит следующим образом.
try:
   foo()
except <имя 1>:
   print("<имя 1>")
except <имя 2>:
   print("<имя 2>")
...


Костя посмотрел на этот код и указал Антону на то, что некоторые исключения можно не ловить, так как ранее в коде
будет пойман их предок. Но Антон не помнит какие исключения наследуются от каких. Помогите ему выйти из неловкого
положения и напишите программу, которая будет определять обработку каких исключений можно удалить из кода.

Важное примечание:
В отличие от предыдущей задачи, типы исключений не созданы.
Создавать классы исключений также не требуется
Мы просим вас промоделировать этот процесс, и понять какие из исключений можно и не ловить, потому что мы уже ранее
где-то поймали их предка.

Формат входных данных

В первой строке входных данных содержится целое число n - число классов исключений.

В следующих n строках содержится описание наследования классов. В i-й строке указано от каких классов наследуется
i-й класс. Обратите внимание, что класс может ни от кого не наследоваться. Гарантируется, что класс не наследуется
сам от себя (прямо или косвенно), что класс не наследуется явно от одного класса более одного раза.

В следующей строке содержится число m - количество обрабатываемых исключений.
Следующие m строк содержат имена исключений в том порядке, в каком они были написаны у Антона в коде.
Гарантируется, что никакое исключение не обрабатывается дважды.

Формат выходных данных

Выведите в отдельной строке имя каждого исключения, обработку которого можно удалить из кода, не изменив при этом
поведение программы. Имена следует выводить в том же порядке, в котором они идут во входных данных.
Пример теста 1

Рассмотрим код

try:
   foo()
except ZeroDivision :
   print("ZeroDivision")
except OSError:
   print("OSError")
except ArithmeticError:
   print("ArithmeticError")
except FileNotFoundError:
   print("FileNotFoundError")

...


По условию этого теста, Костя посмотрел на этот код, и сказал Антону, что исключение FileNotFoundError можно не ловить,
ведь мы уже ловим OSError -- предок FileNotFoundError

Sample Input:
4
ArithmeticError
ZeroDivisionError : ArithmeticError
OSError
FileNotFoundError : OSError
4
ZeroDivisionError
OSError
ArithmeticError
FileNotFoundError

Sample Output:
FileNotFoundError
"""

# Пример использования. В консоли:
# > python 24463_step_7.py < in
# FileNotFoundError

if __name__ == "__main__":
    # Sample Input:
    # 4
    # ArithmeticError
    # ZeroDivisionError : ArithmeticError
    # OSError
    # FileNotFoundError : OSError
    # 4
    # ZeroDivisionError
    # OSError
    # ArithmeticError
    # FileNotFoundError
    #
    # Sample Output:
    # FileNotFoundError

    # По заданию необязательно через классы делать,
    # поэтому можно этот класс заменить словарем вида { 'name': '...', 'parents': [...] }
    # И, соответственно, функцию has_parent вынести из класса и поменять, чтобы она работала с словарем.
    class Class:
        def __init__(self, name) -> None:
            self.name = name
            self.list_parent_class = list()

        def has_parent(self, name) -> bool:
            # Поиск предка в текущем классе
            for parent in self.list_parent_class:
                if parent.name == name:
                    return True

            # Рекурсивный поиск предка у предков текущем классе
            for parent in self.list_parent_class:
                if parent.has_parent(name):
                    return True

            return False

        def __str__(self) -> str:
            return (
                f'Class <"{self.name}": {[cls.name for cls in self.list_parent_class]}>'
            )

        def __repr__(self) -> str:
            return self.__str__()

    from collections import OrderedDict, defaultdict

    class_dict = OrderedDict()

    # Словарь, в котором по ключу находится объект класса, а по
    # значению -- список названий (строка) классов, от которых от наследуется
    class_line_dict = defaultdict(list)

    # Алгоритм:
    #  * Нахождение всех классов и добавление их в class_dict
    #  * Если у класса указано наследование, добавление названия (строка) предков в class_line_dict
    #  * После нахождения всех классов, выполняется перебор class_line_dict, чтобы заполнить список
    #    предков найденных классов. К этому моменту всевозможные классы уже будут храниться в class_dict

    n = int(input())
    for _ in range(n):
        s = input()
        # print(s)

        clsn = s.split(" : ")
        cls1_name = clsn[0]

        # Добавление класса в словарь
        cls = Class(cls1_name)
        class_dict[cls1_name] = cls

        # Попалось описание с наследованием
        if len(clsn) == 2:
            class_line_dict[cls] += clsn[1].split()

    for cls, names_cls_list in class_line_dict.items():
        for name_cls in names_cls_list:
            cls.list_parent_class.append(class_dict[name_cls])

    # Список вызовов исключений
    list_exc = list()

    # Заполнение списка вызовов исключений
    n = int(input())
    for _ in range(n):
        list_exc.append(input())

    # Чтобы не было повторов, используем для хранения множество
    unnecessary_list = list()

    # На каждый вызов исключений делается проверка на то, что другое исключение из списка
    # является его предком и его индекс меньше (был вызван раньше)
    for i, exc in enumerate(list_exc):
        for j, exc2 in enumerate(list_exc):
            if class_dict[exc].has_parent(exc2) and j < i:
                if exc not in unnecessary_list:
                    unnecessary_list.append(exc)

    for exc in unnecessary_list:
        print(exc)
