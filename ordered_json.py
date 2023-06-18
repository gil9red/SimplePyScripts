#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://stackoverflow.com/a/6921760/5909792
# SOURCE: https://stackoverflow.com/a/23820416/5909792

import json
from collections import OrderedDict


json_data = {"foo": 1, "bar": 2, "abc": {"a": 1, "b": 2, "c": 3}}

ordered_json_data = OrderedDict()
ordered_json_data["foo"] = 1
ordered_json_data["bar"] = 2
ordered_json_data["abc"] = OrderedDict()
ordered_json_data["abc"]["a"] = 1
ordered_json_data["abc"]["b"] = 2
ordered_json_data["abc"]["c"] = 3

print("Dumps:")

print(json.dumps(json_data, indent=4))
# {
#     "bar": 2,
#     "abc": {
#         "a": 1,
#         "b": 2,
#         "c": 3
#     },
#     "foo": 1
# }

ordered_json_str = json.dumps(ordered_json_data, indent=4)
print(ordered_json_str)
# {
#     "foo": 1,
#     "bar": 2,
#     "abc": {
#         "a": 1,
#         "b": 2,
#         "c": 3
#     }
# }

print()
print("Loads:")

data = json.loads(ordered_json_str)
print(json.dumps(data, indent=4))
# {
#     "bar": 2,
#     "abc": {
#         "c": 3,
#         "b": 2,
#         "a": 1
#     },
#     "foo": 1
# }

data = json.loads(ordered_json_str, object_pairs_hook=OrderedDict)
print(json.dumps(data, indent=4))
# {
#     "foo": 1,
#     "bar": 2,
#     "abc": {
#         "a": 1,
#         "b": 2,
#         "c": 3
#     }
# }
