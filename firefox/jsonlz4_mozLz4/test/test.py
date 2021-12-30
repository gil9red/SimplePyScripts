#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import io
import sys
import unittest
import uuid

from pathlib import Path


DIR = Path(__file__).resolve().parent

sys.path.append(str(DIR.parent))
import mozlz4a


FILE_TEST = DIR / 'recovery.jsonlz4'


# f_lz4 = open(file_name_session_lz4, 'rb')
# data = mozlz4a.decompress(f_lz4)
# print(data)
#
# compressed_data = open(file_name_session_lz4, 'rb').read()
# print(len(compressed_data))
# data = mozlz4a.decompress_data(compressed_data)
# print(len(data), data)
# print(str(data, 'utf-8'))
#
# import json
# # json_data = json.loads(data)
# json_data = mozlz4a.load_json(file_name_session_lz4)
# print(json_data)
# assert json.loads(data) == json_data
# print()
#
# for w in json_data['windows']:
#     for t in w['tabs']:
#         i = t['index'] - 1
#         # t['entries'][i]['title'],
#         print(i, t['entries'][i]['url'])
#


class TestAll(unittest.TestCase):
    def test_exists_file(self):
        self.assertTrue(FILE_TEST.exists())
        self.assertTrue(FILE_TEST.read_bytes())

    def test_decompress_compress(self):
        with open(FILE_TEST, 'rb') as f:
            expected_data = mozlz4a.decompress(f)

        bytes_io = io.BytesIO(expected_data)
        compressed_data = mozlz4a.compress(bytes_io)

        compressed_bytes_io = io.BytesIO(compressed_data)
        data = mozlz4a.decompress(compressed_bytes_io)

        self.assertEqual(expected_data, data)

    def test_compress_decompress_data(self):
        expected_data = str(uuid.uuid4()).encode('utf-8')

        compressed_data = mozlz4a.compress_data(expected_data)
        data = mozlz4a.decompress_data(compressed_data)

        self.assertEqual(expected_data, data)

    def test_json(self):
        with open(FILE_TEST, 'rb') as f:
            expected_json_data = mozlz4a.loads_json(f)

        bytes_io = io.BytesIO()
        mozlz4a.dumps_json(bytes_io, expected_json_data)

        bytes_io.seek(0)
        json_data = mozlz4a.loads_json(bytes_io)

        self.assertEqual(expected_json_data, json_data)


if __name__ == '__main__':
    unittest.main()
