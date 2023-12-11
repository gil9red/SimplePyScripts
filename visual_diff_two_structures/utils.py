#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json

try:
    from collections.abc import MutableMapping
except ImportError:
    from collections import MutableMapping

# pip install xmltodict
import xmltodict


def get_filling_in_missing(
    items_1: list[str],
    items_2: list[str],
    fill_empty_spaces: bool = False,
) -> tuple[list[str], list[str]]:
    common_keys = sorted(set(items_1 + items_2))

    result_1: list[str] = []
    result_2: list[str] = []

    for key in common_keys:
        empty = (" " * len(key)) if fill_empty_spaces else ""

        result_1.append(key if key in items_1 else empty)
        result_2.append(key if key in items_2 else empty)

    return result_1, result_2


# SOURCE: https://stackoverflow.com/a/6027615/5909792
def flatten(dictionary: MutableMapping, parent_key: str = '', separator: str = '_'):
    items: list[tuple] = []
    for key, value in dictionary.items():
        new_key = parent_key + separator + key if parent_key else key
        if isinstance(value, MutableMapping):
            items.extend(flatten(value, new_key, separator=separator).items())
        else:
            items.append((new_key, value))
    return dict(items)


def xml_to_flatten_dict(xml_str: str) -> dict:
    dict_xml = xmltodict.parse(xml_str)
    return flatten(dict_xml, separator="/")


def json_to_flatten_dict(json_str: str) -> dict:
    dict_json = json.loads(json_str)
    return flatten(dict_json, separator="/")


if __name__ == "__main__":
    items_1 = ["F1", "F2", "F3/SF1", "F3/SF2", "F4", "F3", "F6", "F7"]
    items_2 = ["F3/SF1", "F5", "F3", "F6"]
    result_1, result_2 = get_filling_in_missing(items_1, items_2, fill_empty_spaces=True)
    print(result_1)
    print(result_2)
    assert result_1 == ["F1", "F2", "F3", "F3/SF1", "F3/SF2", "F4", "  ", "F6", "F7"]
    assert result_2 == ["  ", "  ", "F3", "F3/SF1", "      ", "  ", "F5", "F6", "  "]

    print()

    items_1 = ["F1", "F2", "F3/SF1", "F3/SF2", "F4", "F3", "F6", "F7", "F8", "F9"]
    items_2 = ["F3/SF1", "F5", "F3", "F6", "F99"]
    print(items_1)
    print(items_2)
    print()
    result_1, result_2 = get_filling_in_missing(items_1, items_2, fill_empty_spaces=True)
    print(result_1)
    print(result_2)
    assert result_1 == ['F1', 'F2', 'F3', 'F3/SF1', 'F3/SF2', 'F4', '  ', 'F6', 'F7', 'F8', 'F9', '   ']
    assert result_2 == ['  ', '  ', 'F3', 'F3/SF1', '      ', '  ', 'F5', 'F6', '  ', '  ', '  ', 'F99']

    print()

    dict_data = {'a': 1, 'c': {'a': 2, 'b': {'x': 5, 'y' : 10}}, 'd': [1, 2, 3]}
    actual_dict = flatten(dict_data, separator="/")
    expected_dict = {'a': 1, 'c/a': 2, 'c/b/x': 5, 'd': [1, 2, 3], 'c/b/y': 10}
    assert actual_dict == expected_dict

    xml_str = """
<mydocument has="an attribute">
  <and>
    <many>elements</many>
    <many>more elements</many>
  </and>
  <plus a="complex">element as well</plus>
  <comment>Hello World!</comment>
</mydocument>
    """
    dict_xml = xmltodict.parse(xml_str)
    print(dict_xml)
    assert dict_xml == {'mydocument': {'@has': 'an attribute', 'and': {'many': ['elements', 'more elements']}, 'plus': {'@a': 'complex', '#text': 'element as well'}, 'comment': 'Hello World!'}}

    dict_xml_flatten = flatten(dict_xml, separator="/")

    expected_dict_flatten = {'mydocument/@has': 'an attribute', 'mydocument/and/many': ['elements', 'more elements'], 'mydocument/plus/@a': 'complex', 'mydocument/plus/#text': 'element as well', 'mydocument/comment': 'Hello World!'}
    actual_dict_flatten = xml_to_flatten_dict(xml_str)
    print(actual_dict_flatten)
    assert actual_dict_flatten == expected_dict_flatten

    json_str = """
{
    "mydocument": {
        "@has": "an attribute",
        "and": {
            "many": [
                "elements",
                "more elements"
            ]
        },
        "plus": {
            "@a": "complex",
            "#text": "element as well"
        },
        "comment": "Hello World!"
    }
}
    """
    assert json_to_flatten_dict(json_str) == expected_dict_flatten
