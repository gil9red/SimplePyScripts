__author__ = "ipetrash"


# Если вызывать функцию plot() несколько раз подряд, то на график
# будут добавляться новые кривые. Следующий пример рисует два графика на одних осях:

import math

# !!! Импортируем один из пакетов Matplotlib
import pylab

# !!! Импортируем пакет со вспомогательными функциями
from matplotlib__examples import mlab

if __name__ == "__main__":
    # Будем рисовать график этой функции
    def func(x):
        """
        sinc (x)
        """
        if x == 0:
            return 1.0
        return math.sin(x) / x

    # Интервал изменения переменной по оси X
    xmin = -20.0
    xmax = 20.0

    # Шаг между точками
    dx = 0.01

    # !!! Создадим список координат по оиси X на отрезке [-xmin; xmax], включая концы
    xlist = mlab.frange(xmin, xmax, dx)

    # Вычислим значение функции в заданных точках
    ylist1 = [func(x) for x in xlist]
    ylist2 = [func(x * 0.2) for x in xlist]

    # !!! Нарисуем одномерные графики
    pylab.plot(xlist, ylist1)
    pylab.plot(xlist, ylist2)

    # !!! Покажем окно с нарисованным графиком
    pylab.show()
