__author__ = "ipetrash"


# Цветовые карты используются, если нужно указать в какие цвета должны окрашиваться
# участки трехмерной поверхности в зависимости от значения Z в этой области (задание
# цветового градиента). Тема использование градиентов сама по себе большая и интересная,
# но мы сейчас рассмотрим только некоторые ее аспекты. Чтобы при выводе графика
# использовался градиент, в качестве значения параметра cmap (от слова colormap, цветовая
# карта) нужно передать экземпляр класса matplotlib.colors.Colormap или производного от него.
# Следующий пример использует класс LinearSegmentedColormap, производный от Colormap,
# чтобы создать градиент перехода от синего цвета к красному через белый.


import numpy
import pylab

from mpl_toolkits.mplot3d import Axes3D
from matplotlib__examples.colors import LinearSegmentedColormap


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

    # Здесь используется статический метод from_list(), который принимает три параметра:
    # Имя создаваемой карты
    # Список цветов, начиная с цвета для минимального значения на графике (голубой - 'b'),
    # через промежуточные цвета (у нас это белый - 'w') к цвету для максимального значения
    # функции (красный - 'r').
    # Количество цветовых переходов. Чем это число больше, тем более плавный градиент, но
    # тем больше памяти он занимает.
    # Если вы не хотите каждый раз создавать свою цветовую карту, то можете воспользоваться
    # одной из уже готовых карт, которые располагаются в модуле matplotlib.cm.
    # Чтобы узнать какие цветовые карты существуют, можно просто прочитать переменную cm._
    # cmapnames, которая представляет собой список строк:
    # from matplotlib import cm
    # print(cm.cmap_d)
    #
    # from matplotlib import cm
    # color_map = cm.cmap_d["jet"]
    # axes.plot_surface(x, y, z, rstride=4, cstride=4, cmap=color_map)

    color_map = LinearSegmentedColormap.from_list("red_blue", ["b", "w", "r"], 256)
    axes.plot_surface(x, y, z, rstride=3, cstride=3, cmap=color_map)

    pylab.show()
