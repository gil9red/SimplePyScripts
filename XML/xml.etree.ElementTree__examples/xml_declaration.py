#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://docs.python.org/3/library/xml.etree.elementtree.html

import io
import xml.etree.ElementTree as ET

from pretty_print import indent


root = ET.Element("data")

country = ET.Element("country", name="Liechtenstein")

rank = ET.Element("rank", updated="yes")
rank.text = "2"
country.append(rank)

root.append(country)

indent(root)

xml_str = ET.tostring(root, encoding="utf-8", method="xml")
print(xml_str.decode(encoding="utf-8"))
# <data>
#   <country name="Liechtenstein">
#     <rank updated="yes">2</rank>
#   </country>
# </data>

etree = ET.ElementTree(root)
f = io.BytesIO()
etree.write(f, encoding="utf-8", xml_declaration=True)
print(f.getvalue().decode(encoding="utf-8"))
# <?xml version='1.0' encoding='utf-8'?>
# <data>
#   <country name="Liechtenstein">
#     <rank updated="yes">2</rank>
#   </country>
# </data>
