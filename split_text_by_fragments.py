#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def split_text_by_fragments(text: str, fragment_length=50) -> list:
    """
    Функция для разбития текста (<text>) на куски указанной длины (<fragment_length>).

    """

    # Если длина фрагмента больше или равна длине текста, то сразу возвращаем список из одного элемента
    if fragment_length >= len(text):
        return [text]

    fragments = list()

    # Количество фрагментов
    number = len(text) // fragment_length + 1

    for i in range(number):
        start = fragment_length * i
        end = fragment_length * (i + 1)

        fragments.append(text[start:end])

    return fragments


if __name__ == "__main__":
    text = """\
Брату в пору башмаки:
Не малы, не велики.

Их надели на Андрюшку,
Но ни с места он пока -
Он их принял за игрушку,
Глаз не сводит с башмака.

Мальчик с толком, с расстановкой
Занимается обновкой:
То погладит башмаки,
То потянет за шнурки.

Сел Андрей и поднял ногу,
Языком лизнул башмак...
Ну, теперь пора в дорогу,
Можно сделать первый шаг!
"""

    fragments = split_text_by_fragments(text)
    print(len(fragments), fragments)
    assert "".join(fragments) == text
    assert len(fragments) == 7

    fragments = split_text_by_fragments(text, fragment_length=len(text))
    print(len(fragments), fragments)
    assert "".join(fragments) == text
    assert len(fragments) == 1

    fragments = split_text_by_fragments(text, fragment_length=9999)
    print(len(fragments), fragments)
    assert "".join(fragments) == text
    assert len(fragments) == 1
