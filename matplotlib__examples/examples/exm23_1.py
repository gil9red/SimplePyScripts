__author__ = "ipetrash"


## Использование библиотеки Matplotlib. Как изменять формат меток на осях
## Введение
#
# Помимо настройки положения меток на осях Matplotlib позволяет настраивать
# подписи под ними. Для этого используются специальные классы (форматеры),
# производные от класса matplotlib.ticker.Formatter. Для того, чтобы установить
# форматер для оси, нужно вызвать метод set_major_formatter() экземпляра класса
# matplotlib.axis.Axis - класса для работы с одной осью.
# Для начала выведем график, в котором используется форматирование подписей по
# умолчанию.


import numpy

import pylab


if __name__ == "__main__":
    xvals = numpy.arange(-10.0, 10.1, 0.1)
    yvals = numpy.sinc(xvals)

    figure = pylab.figure()
    axes = figure.add_subplot(1, 1, 1)

    pylab.plot(xvals, yvals)

    axes.grid()
    pylab.show()
