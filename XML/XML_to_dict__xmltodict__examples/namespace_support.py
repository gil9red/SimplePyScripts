#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/martinblech/xmltodict#namespace-support


import json

# pip install xmltodict
import xmltodict


# By default, xmltodict does no XML namespace processing (it just treats namespace declarations as regular
# node attributes), but passing process_namespaces=True will make it expand namespaces for you:
xml = """
<root xmlns="http://defaultns.com/"
      xmlns:a="http://a.com/"
      xmlns:b="http://b.com/">
  <x>1</x>
  <a:y>2</a:y>
  <b:z>3</b:z>
</root>
"""
doc = xmltodict.parse(xml, process_namespaces=True)

print(json.dumps(doc, indent=4))
# {
#     "http://defaultns.com/:root": {
#         "http://defaultns.com/:x": "1",
#         "http://a.com/:y": "2",
#         "http://b.com/:z": "3"
#     }
# }

print("\n")


# It also lets you collapse certain namespaces to shorthand prefixes, or skip them altogether:
namespaces = {
    "http://defaultns.com/": None,  # skip this namespace
    "http://a.com/": "ns_a",  # collapse "http://a.com/" -> "ns_a"
}
doc = xmltodict.parse(xml, process_namespaces=True, namespaces=namespaces)
print(json.dumps(doc, indent=4))
# {
#     "root": {
#         "x": "1",
#         "ns_a:y": "2",
#         "http://b.com/:z": "3"
#     }
# }
