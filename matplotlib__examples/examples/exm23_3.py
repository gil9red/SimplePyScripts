__author__ = "ipetrash"


## FormatStrFormatter
#
# По осям в большинстве случаев откладываются какие-либо числовые данные
# (календарный тип данных заслуживает отдельной статьи), поэтому логично
# предоставить пользователям класс для удобного выбора числового формата
# надписей (количество знакомест, количество значащих нулей, возможность
# использования экспоненциальной формы записи чисел и т.п.). Для этого и
# предназначен класс FormatStrFormatter.
# В качестве единственного параметра его конструктор принимает строку
# форматирования, в которую при помощи оператора % будут подставляться
# числа, соответствующие меткам.
# В качестве строки форматирования может быть любая строка, благодаря
# чему можно, например, добавлять дополнительные надписи к каждой подписи.
#
# Следующий пример показывает, как использовать этот класс для того,
# чтобы числа по оси X выводились в формате с фиксированной точкой и
# тремя знаками после запятой.


import numpy

import pylab
import matplotlib__examples.ticker


if __name__ == "__main__":
    xvals = numpy.arange(-10.0, 10.1, 0.1)
    yvals = numpy.sinc(xvals)

    pylab.rc("font", **{"family": "verdana"})
    figure = pylab.figure()
    axes = figure.add_subplot(1, 1, 1)

    # Создаем форматер
    formatter = matplotlib__examples.ticker.FormatStrFormatter("%.3f")

    # Установка форматера для оси X
    axes.xaxis.set_major_formatter(formatter)

    pylab.plot(xvals, yvals)

    axes.grid()
    pylab.show()
