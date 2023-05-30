__author__ = "ipetrash"


import numpy
import pylab
from mpl_toolkits.mplot3d import Axes3D


# Эта функция возвращает три двумерные матрицы: x, y, z.
# Координаты x и y лежат в интервале от -10 до 10 с шагом 0.1.
def makeData():
    x = numpy.arange(-10, 10, 0.1)
    y = numpy.arange(-10, 10, 0.1)
    xgrid, ygrid = numpy.meshgrid(x, y)

    zgrid = numpy.sin(xgrid) * numpy.sin(ygrid) / (xgrid * ygrid)
    return xgrid, ygrid, zgrid


if __name__ == "__main__":
    x, y, z = makeData()

    # Чтобы отобразить наши данные, достаточно вызвать метод plot_surface()
    # экземпляра класса Axes3D, в который передадим полученные с помощью
    # функции makeData() двумерные матрицы.
    fig = pylab.figure()
    axes = Axes3D(fig)

    axes.plot_surface(x, y, z)
    # axes.plot_surface(x, y, z, color='yellow')  # Изменение цвета фигуры
    # axes.plot_surface(x, y, z, rstride=5, cstride=5)  # Установка шага сетки (при 5, очень мелкая сетка)
    # axes.plot_surface(x, y, z, rstride=20, cstride=20)  # Установка шага сетки (при 20, крупная сетка)

    pylab.show()
