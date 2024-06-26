__author__ = "ipetrash"


## Использование библиотеки Matplotlib. Более гибкий способ расположения графиков с
# помощью subplot2grid
# До сих пор для того, чтобы в одном окне расположить несколько графиков был только
# один способ - воспользоваться функцией subplot, которой в большинстве случаев вполне
# хватает. Но эта функция обладает одним недостатком - при ее использовании график
# может занимать только одну ячейку некой виртуальной таблицы. Да, для каждого
# графика можно задавать свою таблицу расположения (разное количество строк и
# столбцов), благодаря чему может казаться, что график занимает несколько ячеек,
# но все-равно такой подход довольно ограничен.
# В Matplotlib 1.0.0 появился новый, более гибкий способ расположения графиков с
# помощью фунции subplot2grid, которая позволяет занимать графику несколько ячеек
# таблицы.
#
# В данном примере намеренно не приводится вывод самого графика, чтобы сосредоточить
# внимание на использовании функции subplot2grid. Все комментарии по использованию
# subplot2grid даны в тексте скрипта.


# Импортируем один из пакетов Matplotlib
import pylab


if __name__ == "__main__":
    # Таблица графиков будет иметь три строки и три столбца (3,3)

    # Вывод будет осуществляться в ячейку с координатами (0, 0),
    # то есть 0-ая строка и 0-ой столбец
    # Оси для графика будут занимать две ячейки по горизонтали (colspan = 2)
    # и две ячейки по вертикали (rowspan = 2)
    pylab.subplot2grid((3, 3), (0, 0), colspan=2, rowspan=2)
    pylab.title("Graph1")

    # Вывод будет осуществляться в ячейку с координатами (0, 2),
    # то есть 0-ая строка и 2-ой столбец (нумерация начинается с нуля)
    # Оси для графика будут занимать две ячейки по вертикали (rowspan = 2)
    pylab.subplot2grid((3, 3), (0, 2), rowspan=2)
    pylab.title("Graph2")

    # Вывод будет осуществляться в ячейку с координатами (2, 0),
    # то есть 2-ая строка и 0-ой столбец
    # Оси для графика будут занимать одну ячейку по вертикали и горизонтали
    # Аналог этого вызова - pylab.subplot (3, 3, 7)
    pylab.subplot2grid((3, 3), (2, 0))
    pylab.title("Graph3")

    # Вывод будет осуществляться в ячейку с координатами (2, 1),
    # то есть 2-ая строка и 1-ый столбец
    # Оси для графика будут занимать две ячейки по горизонтали (colspan = 2)
    pylab.subplot2grid((3, 3), (2, 1), colspan=2)
    pylab.title("Graph4")

    pylab.show()
