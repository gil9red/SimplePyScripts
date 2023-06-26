__author__ = "ipetrash"


## FuncFormatter
#
# Логичным продолжением FormatStrFormatter является класс FuncFormatter,
# который позволяет еще более гибко настраивать формат меток с помощью
# функции, которая будет возвращать строковое представление каждой метки.
# В качестве единственного параметра конструктора FuncFormatter принимает
# эту самую функцию, которая, в свою очередь, ожидает два параметра:
# def funcForFormatter (x, pos):
#     ...
# Исходник
# Параметр x представляет собой величину, которую нужно отобразить около
# метки, а параметр pos - это номер метки: 0, 1, 2,...
# Эта функция должна вернуть строку, которая будет отображаться около
# соответствующей метки.
# Обратите внимание, что здесь изменен шрифт на Verdana, чтобы не было
# проблем с русскими буквами
#
# В следующем примере FuncFormatter используется для того, чтобы выводить
# числа в виде "плюс 10", "минус 5" и т.п.


import numpy

import pylab
import matplotlib__examples.ticker


def funcForFormatter(x, pos):
    if x < 0:
        return f"минус {abs(x)}"

    if x > 0:
        return f"плюс {x}"

    return "0"


if __name__ == "__main__":
    xvals = numpy.arange(-10.0, 10.1, 0.1)
    yvals = numpy.sinc(xvals)

    pylab.rc("font", **{"family": "verdana"})
    figure = pylab.figure()
    axes = figure.add_subplot(1, 1, 1)

    # Создаем форматер
    formatter = matplotlib__examples.ticker.FuncFormatter(funcForFormatter)

    # Установка форматера для оси X
    axes.xaxis.set_major_formatter(formatter)

    pylab.plot(xvals, yvals)

    axes.grid()
    pylab.show()
