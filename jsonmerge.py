#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json


json_str_1 = """
{
   "Comment":"My comment",
   "Count":10,
   "Errors": null,
   "DiskParam":
   {
     "DB":10.000000,
     "DBAngle":1.234000
   }
}
"""

json_str_2 = """
{
  "Comment":"My super comment!",
  "Count":20,
  "Errors": "@##@##%!",
  "DiskParam":
  {
    "DB":42,
    "Foo": [1, 2, 3, 4]
  }
}
"""

json_1 = json.loads(json_str_1)
json_2 = json.loads(json_str_2)
print(json_1)
print(json_2)


# TODO: нужно тестить, возможно, алгоритм где-то дырявый
def jsonmerge(j1, j2) -> None:
    for k, v in j2.items():
        if k in j1 and isinstance(j1[k], dict) and isinstance(v, dict):
            jsonmerge(j1[k], v)
        else:
            j1[k] = v


jsonmerge(json_1, json_2)
print(json_1)
print(json.dumps(json_1, indent=4))
