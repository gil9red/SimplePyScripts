#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import unittest
import utils


class TestCaseUtils(unittest.TestCase):
    def test_get_filling_in_missing(self):
        items_1 = ["F1", "F2", "F3/SF1", "F3/SF2", "F4", "F3", "F6", "F7"]
        items_2 = ["F3/SF1", "F5", "F3", "F6"]

        with self.subTest(items_1=items_1, items_2=items_2, fill_empty_spaces=True):
            result_1, result_2 = utils.get_filling_in_missing(
                items_1, items_2, fill_empty_spaces=True
            )
            self.assertEqual(
                result_1, ["F1", "F2", "F3", "F3/SF1", "F3/SF2", "F4", "  ", "F6", "F7"]
            )
            self.assertEqual(
                result_2, ["  ", "  ", "F3", "F3/SF1", "      ", "  ", "F5", "F6", "  "]
            )

        with self.subTest(
            items_1=items_1, items_2=items_2, fill_empty_spaces="<default>"
        ):
            result_1, result_2 = utils.get_filling_in_missing(items_1, items_2)
            self.assertEqual(
                result_1, ["F1", "F2", "F3", "F3/SF1", "F3/SF2", "F4", "", "F6", "F7"]
            )
            self.assertEqual(result_2, ["", "", "F3", "F3/SF1", "", "", "F5", "F6", ""])

        with self.subTest(items_1=items_1, items_2=items_2, fill_empty_spaces=False):
            result_1, result_2 = utils.get_filling_in_missing(
                items_1, items_2, fill_empty_spaces=False
            )
            self.assertEqual(
                result_1, ["F1", "F2", "F3", "F3/SF1", "F3/SF2", "F4", "", "F6", "F7"]
            )
            self.assertEqual(result_2, ["", "", "F3", "F3/SF1", "", "", "F5", "F6", ""])

        with self.subTest(items_1="<empty>", items_2=items_2, fill_empty_spaces=True):
            result_1, result_2 = utils.get_filling_in_missing(
                [], items_2, fill_empty_spaces=True
            )
            self.assertEqual(result_1, ["  ", "      ", "  ", "  "])
            self.assertEqual(result_2, ["F3", "F3/SF1", "F5", "F6"])

        with self.subTest(items_1=items_1, items_2="<empty>", fill_empty_spaces=True):
            result_1, result_2 = utils.get_filling_in_missing(
                items_1, [], fill_empty_spaces=True
            )
            self.assertEqual(
                result_1, ["F1", "F2", "F3", "F3/SF1", "F3/SF2", "F4", "F6", "F7"]
            )
            self.assertEqual(
                result_2, ["  ", "  ", "  ", "      ", "      ", "  ", "  ", "  "]
            )

        with self.subTest(items_1="<empty>", items_2="<empty>", fill_empty_spaces=True):
            result_1, result_2 = utils.get_filling_in_missing(
                [], [], fill_empty_spaces=True
            )
            self.assertEqual(result_1, [])
            self.assertEqual(result_2, [])

        with self.subTest(items_1="None", items_2="None", fill_empty_spaces=True):
            with self.assertRaises(TypeError):
                utils.get_filling_in_missing(None, None, fill_empty_spaces=True)

        with self.subTest(items_1=items_1, items_2="None", fill_empty_spaces=True):
            with self.assertRaises(TypeError):
                utils.get_filling_in_missing(items_1, None, fill_empty_spaces=True)

        with self.subTest(items_1=items_1, items_2=items_2, fill_empty_spaces=True):
            with self.assertRaises(TypeError):
                utils.get_filling_in_missing(None, items_2, fill_empty_spaces=True)

        with self.subTest(items_1=items_1, items_2=items_1, fill_empty_spaces=True):
            result_1, result_2 = utils.get_filling_in_missing(
                items_1, items_1, fill_empty_spaces=True
            )
            self.assertEqual(
                result_1, ["F1", "F2", "F3", "F3/SF1", "F3/SF2", "F4", "F6", "F7"]
            )
            self.assertEqual(
                result_2, ["F1", "F2", "F3", "F3/SF1", "F3/SF2", "F4", "F6", "F7"]
            )

        with self.subTest(
            items_1=items_1,
            items_2=["F1", "F7", "F2", "F3", "F6", "F3/SF1", "F3/SF2", "F4"],
            fill_empty_spaces=True,
        ):
            result_1, result_2 = utils.get_filling_in_missing(
                items_1, items_1, fill_empty_spaces=True
            )
            self.assertEqual(
                result_1, ["F1", "F2", "F3", "F3/SF1", "F3/SF2", "F4", "F6", "F7"]
            )
            self.assertEqual(
                result_2, ["F1", "F2", "F3", "F3/SF1", "F3/SF2", "F4", "F6", "F7"]
            )

        items_1 = ["F1", "F2", "F3"]
        items_2 = ["F4", "F5", "F6"]

        with self.subTest(items_1=items_1, items_2=items_2, fill_empty_spaces=True):
            result_1, result_2 = utils.get_filling_in_missing(
                items_1, items_2, fill_empty_spaces=True
            )
            self.assertEqual(result_1, ["F1", "F2", "F3", "  ", "  ", "  "])
            self.assertEqual(result_2, ["  ", "  ", "  ", "F4", "F5", "F6"])

    def test_flatten(self):
        dict_data = {"a": 1, "c": {"a": 2, "b": {"x": 5, "y": 10}}, "d": [1, 2, 3]}
        actual_dict = utils.flatten(dict_data, separator="/")
        expected_dict = {"a": 1, "c/a": 2, "c/b/x": 5, "d": [1, 2, 3], "c/b/y": 10}
        self.assertEqual(actual_dict, expected_dict)

    def test_xml_to_flatten_dict(self):
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

        expected_dict_flatten = {
            "mydocument/@has": "an attribute",
            "mydocument/and/many": ["elements", "more elements"],
            "mydocument/plus/@a": "complex",
            "mydocument/plus/#text": "element as well",
            "mydocument/comment": "Hello World!",
        }
        actual_dict_flatten = utils.xml_to_flatten_dict(xml_str)
        self.assertEqual(actual_dict_flatten, expected_dict_flatten)

    def test_json_to_flatten_dict(self):
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
        expected_dict_flatten = {
            "mydocument/@has": "an attribute",
            "mydocument/and/many": ["elements", "more elements"],
            "mydocument/plus/@a": "complex",
            "mydocument/plus/#text": "element as well",
            "mydocument/comment": "Hello World!",
        }
        self.assertEqual(utils.json_to_flatten_dict(json_str), expected_dict_flatten)


if __name__ == "__main__":
    unittest.main()
