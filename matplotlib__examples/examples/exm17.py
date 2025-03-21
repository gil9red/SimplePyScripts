__author__ = "ipetrash"


## Использование библиотеки Matplotlib. Как нарисовать несколько графиков в одном окне
# Часто бывает удобно отобразить несколько независимых графиков в одном окне. Для
# этого предназначена функция subplot() из пакета "'pylab''.
# У этой функции есть несколько вариантов ее использования, которые отличаются
# только лишь способом передачи параметров. Мы рассмотрим только один из них.
# Функция subplot() ожидает три параметра:
#     количество строк в графике;
#     количество столбцов в графике;
#     номер ячейки, куда будут выводиться графики, после вызова этой функции.
# Ячейки нумеруются построчно, начиная с 1.
# Проще всего сразу рассмотреть пример. В этом примере для простоты будут выводиться
# одинаковые графики в разные ячейки. Чтобы было более наглядно, в заголовок каждого
# графика будет добавлена цифра, обозначающая порядковый номер ячейки.


import math

# Импортируем один из пакетов Matplotlib
import pylab

# Импортируем пакет со вспомогательными функциями
from matplotlib__examples import mlab


# Будем рисовать график этой функции
def func(x):
    """
    sinc (x)
    """
    if x == 0:
        return 1.0
    return math.sin(x) / x


if __name__ == "__main__":
    # Интервал изменения переменной по оси X
    xmin = -20.0
    xmax = 20.0

    # Шаг между точками
    dx = 0.01

    # Создадим список координат по оиси X на отрезке [-xmin; xmax], включая концы
    xlist = mlab.frange(xmin, xmax, dx)

    # Вычислим значение функции в заданных точках
    ylist = [func(x) for x in xlist]

    # !!! Две строки, три столбца.
    # !!! Текущая ячейка - 1
    pylab.subplot(2, 3, 1)
    pylab.plot(xlist, ylist)
    pylab.title("1")

    # !!! Две строки, три столбца.
    # !!! Текущая ячейка - 2
    pylab.subplot(2, 3, 2)
    pylab.plot(xlist, ylist)
    pylab.title("2")

    # !!! Две строки, три столбца.
    # !!! Текущая ячейка - 4
    pylab.subplot(2, 3, 4)
    pylab.plot(xlist, ylist)
    pylab.title("4")

    # !!! Две строки, три столбца.
    # !!! Текущая ячейка - 5
    pylab.subplot(2, 3, 5)
    pylab.plot(xlist, ylist)
    pylab.title("5")

    # !!! Одна строка, три столбца.
    # !!! Текущая ячейка - 3
    pylab.subplot(1, 3, 3)
    pylab.plot(xlist, ylist)
    pylab.title("3")

    # Покажем окно с нарисованным графиком
    pylab.show()
