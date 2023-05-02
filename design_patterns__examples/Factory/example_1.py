#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://ru.wikipedia.org/wiki/Фабричный_метод_(шаблон_проектирования)


from abc import ABC, abstractmethod


class Parser(ABC):
    @abstractmethod
    def parse(self, data: str) -> object:
        pass


class ParserFactory:
    @staticmethod
    def get_parser(name_parser: str) -> Parser:
        if name_parser == "XML":
            return ParserXML()

        elif name_parser == "JSON":
            return ParserJSON()

        elif name_parser == "CSV":
            return ParserCSV()

        raise Exception(f'Unsupported parser "{name_parser}"')


class ParserXML(Parser):
    def parse(self, data: str) -> object:
        from bs4 import BeautifulSoup

        root = BeautifulSoup(data, "xml")
        return root


class ParserJSON(Parser):
    def parse(self, data: str) -> object:
        import json

        return json.loads(data)


class ParserCSV(Parser):
    def parse(self, data: str) -> object:
        import csv

        csv_reader = csv.reader(data.splitlines(), delimiter=";")
        return list(csv_reader)


if __name__ == "__main__":
    result = ParserFactory.get_parser("XML").parse("<a><b>123</b></a>")
    print(result)  # '<?xml version="1.0" encoding="utf-8"?>\n<a><b>123</b></a>'

    json_parser = ParserFactory.get_parser("JSON")
    result = json_parser.parse("[null, null, null]")
    print(result)  # [None, None, None]

    result = json_parser.parse('["a", ["b", "c"], null]')
    print(result)  # ['a', ['b', 'c'], None]

    csv_parser = ParserFactory.get_parser("CSV")
    result = csv_parser.parse("1;vasya;moscow;11111\n2;oleg;sochi;22222")
    print(result)
    # [['1', 'vasya', 'moscow', '11111'], ['2', 'oleg', 'sochi', '22222']]
