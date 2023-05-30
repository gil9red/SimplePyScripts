__author__ = "ipetrash"


## ScalarFormatter
#
# Класс ScalarFormatter используется для простого вывода чисел. При этом у него
# есть несколько настроек, позволяющих сделать отображение больших чисел чуть
# более компактным. Именно этот форматер используется для отображения чисел по
# умолчанию (если не установлен никакой другой форматер).
# Для начала, пусть наша функция sinc() умножается на большое число (например,
# на 105).


import numpy

import pylab


if __name__ == "__main__":
    xvals = numpy.arange(-10.0, 10.1, 0.1)
    yvals = numpy.sinc(xvals) * 1e5

    figure = pylab.figure()
    axes = figure.add_subplot(1, 1, 1)

    pylab.plot(xvals, yvals)

    axes.grid()
    pylab.show()
