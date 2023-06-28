#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://docs.python.org/3/library/xml.etree.elementtree.html

import xml.etree.ElementTree as ET


# SOURCE: http://effbot.org/zone/element-lib.htm#prettyprint
def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


if __name__ == "__main__":
    root = ET.Element("data")

    country = ET.Element("country", name="Liechtenstein")
    rank = ET.Element("rank", updated="yes")
    rank.text = "2"
    country.append(rank)

    root.append(country)

    xml_str = ET.tostring(root, encoding="utf-8", method="xml")
    print(xml_str.decode(encoding="utf-8"))
    # <data><country name="Liechtenstein"><rank updated="yes">2</rank></country></data>

    indent(root)
    xml_str = ET.tostring(root, encoding="utf-8", method="xml")
    print(xml_str.decode(encoding="utf-8"))
    # <data>
    #   <country name="Liechtenstein">
    #     <rank updated="yes">2</rank>
    #   </country>
    # </data>
