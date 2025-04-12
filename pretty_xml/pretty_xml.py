#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from xml.dom.minidom import parseString
from lxml import etree


def process_xml_string(xml_string: str) -> str:
    """
    Функция из текста выдирает строку с xml --
    она должна начинаться на < и заканчиваться >

    """

    start = xml_string.index("<")
    end = xml_string.rindex(">")
    return xml_string[start : end + 1]


def pretty_xml_minidom(xml_string: str, indent: int = 4) -> str:
    """Функция принимает строку xml и выводит xml с отступами."""

    xml_string = process_xml_string(xml_string)
    xml_utf8 = parseString(xml_string).toprettyxml(
        indent=" " * indent,
        encoding="utf-8",
    )
    return xml_utf8.decode("utf-8")


def pretty_xml_lxml(xml_string: str) -> str:
    """Функция принимает строку xml и выводит xml с отступами."""

    xml_string = process_xml_string(xml_string)
    root = etree.fromstring(xml_string)
    return etree.tostring(
        root,
        pretty_print=True,
        encoding="utf-8",
    ).decode("utf-8")


if __name__ == "__main__":
    xml = "<a><b/><c><z/><h/></c></a>"
    print(pretty_xml_minidom(xml))
    print(pretty_xml_lxml(xml))
