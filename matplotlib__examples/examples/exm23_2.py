__author__ = "ipetrash"


# Теперь рассмотрим, как можно менять форматирование с помощью метода
# set_major_formatter(), а заодно посмотрим, какие форматеры предоставляет
# библиотека Matplotlib. Все рассматриваемые здесь форматеры находятся в модуле
# matplotlib.ticker. Кроме того некоторые другие, более специфические модули
# предоставляют свои форматеры (например, модуль для работы с календарными данными),
# но в данной статье мы их рассматривать не будем.
# NullFormatter
#
# С помощью класса NullFormatter можно отключить вывод всех подписей у меток на
# оси (при этом сами метки остаются, для их отключения нужно использовать локатор
# NullLocator).


import numpy

import pylab
import matplotlib__examples.ticker


if __name__ == "__main__":
    xvals = numpy.arange(-10.0, 10.1, 0.1)
    yvals = numpy.sinc(xvals)

    figure = pylab.figure()
    axes = figure.add_subplot(1, 1, 1)

    # Создаем форматер
    formatter = matplotlib__examples.ticker.NullFormatter()

    # Установка форматера для оси X
    axes.xaxis.set_major_formatter(formatter)

    pylab.plot(xvals, yvals)

    axes.grid()
    pylab.show()
