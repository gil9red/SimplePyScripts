__author__ = "ipetrash"


## FixedFormatter
#
# Если заранее известно количество меток, то может оказаться полезным форматер
# FixedFormatter для задания нестандартных надписей под ними.
# Конструктор FixedFormatter принимает список строк, и эти строки последовательно
# подписывает под соответствующей меткой.
#
# Если же переданных подписей оказывается больше, чем рисок, то в этом нет ничего
# страшного, "лишние" подписи игнорируются.
#
# Если же меток оказывается больше, чем переданных надписей, то под оставшимися
# метками надпись выводиться не будет.


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
    formatter = matplotlib__examples.ticker.FixedFormatter(
        ["Раз", "Два", "Три", "Четыре", "Пять"]
    )

    # Установка форматера для оси X
    axes.xaxis.set_major_formatter(formatter)

    pylab.plot(xvals, yvals)

    axes.grid()
    pylab.show()
