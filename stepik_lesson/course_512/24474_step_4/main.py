#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Вам дано описание пирамиды из кубиков в формате XML.
Кубики могут быть трех цветов: красный (red), зеленый (green) и синий (blue).
Для каждого кубика известны его цвет, и известны кубики, расположенные прямо под ним.

Пример:
<cube color="blue">
  <cube color="red">
    <cube color="green">
    </cube>
  </cube>
  <cube color="red">
  </cube>
</cube>


Введем понятие ценности для кубиков. Самый верхний кубик, соответствующий корню XML документа имеет ценность 1.
Кубики, расположенные прямо под ним, имеют ценность 2. Кубики, расположенные прямо под нижележащими кубиками, имеют
ценность 3. И т. д.
Ценность цвета равна сумме ценностей всех кубиков этого цвета.

Выведите через пробел три числа: ценности красного, зеленого и синего цветов.

Sample Input:
<cube color="blue"><cube color="red"><cube color="green"></cube></cube><cube color="red"></cube></cube>

Sample Output:
4 3 1

"""


if __name__ == "__main__":
    from collections import defaultdict
    from lxml import etree

    # Ключом является цвет, значением -- сумма ценности
    color_by_price_dict = defaultdict(int)

    def work(element, level=1):
        """Рекурсивная функция для перебора всех элементов и подсчета их ценности."""

        # Плюсуем ценность
        color = element.attrib["color"]
        color_by_price_dict[color] += level

        for child in element:
            work(child, level + 1)

    xml = input()

    root = etree.XML(xml)
    work(root)

    r, g, b = (
        color_by_price_dict["red"],
        color_by_price_dict["green"],
        color_by_price_dict["blue"],
    )
    print(r, g, b)
