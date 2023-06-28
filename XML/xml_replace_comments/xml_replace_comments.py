#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re

from lxml import etree


def replace(file_name, save_file_name):
    with open(file_name, encoding="utf8") as f:
        text = f.read()

        # Ищем закрывающиеся скобки комментариев и удаляем из них многочисленные дефисы, из-за которых
        # xml парсер ругается
        text = re.sub("-{3,}>", "-->", text)

        for match in re.findall("<!--.+?-->", text):
            # Вырезаем текст из тега комментария
            comment_text = match[4:][:-3]

            # Заменяем дефисы одинарным, если они подряд идут от 2 и больше
            comment_text = re.sub("-{2,}", "-", comment_text)
            comment_tag = f"<!--{comment_text}-->"

            if match != comment_tag:
                print(match)
                print("\t", comment_tag, "\n")

                # Делаем замему в тексте
                text = text.replace(match, comment_tag)

        with open(save_file_name, mode="w", encoding="utf8") as f_in:
            f_in.write(text)

        # TODO: уверен есть какой то метож для проверки валидности xml
        # Пытаемся открыть парсером, если не получится, значит xml еще невалидная
        with open(save_file_name, encoding="utf8") as fb2:
            tree = etree.XML(fb2.read().encode())


if __name__ == "__main__":
    # file_name = "Mahouka_Koukou_no_Rettousei_13.fb2"
    # replace(file_name, '_' + file_name)

    # with open("Mahouka_Koukou_no_Rettousei_13.fb2", encoding='utf8') as fb2:
    #     tree = etree.XML(fb2.read().encode(), etree.XMLParser(recover=True))
    #
    #     with open("recover_Mahouka_Koukou_no_Rettousei_13.fb2", mode='wb') as f:
    #         f.write(etree.tostring(tree))
    #     # tree = etree.XML(fb2.read().encode())

    # with open("remove_emphasis_Mahouka_Koukou_no_Rettousei_16.fb2", encoding='utf8') as fb2:
    #     tree = etree.XML(fb2.read().encode())

    # with open("_Mahouka_Koukou_no_Rettousei_16.fb2", encoding='utf8') as fb2:
    #     tree = etree.XML(fb2.read().encode())

    file_name = "Mahouka_Koukou_no_Rettousei_16.fb2"
    replace(file_name, "_" + file_name)

    # for i in range(13, 17):
    #     file_name = "Mahouka_Koukou_no_Rettousei_{}.fb2".format(i)
    # #
    # #     with open(file_name, encoding='utf8') as fb2:
    # #         try:
    # #             tree = etree.XML(fb2.read().encode())
    # #         except:
    # #             print(file_name)
    #     try:
    #         replace(file_name, '_' + file_name)
    #     except Exception as e:
    #         print(file_name, e)
