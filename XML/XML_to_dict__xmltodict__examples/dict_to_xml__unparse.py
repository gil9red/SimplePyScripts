#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/martinblech/xmltodict#roundtripping


# pip install xmltodict
import xmltodict


my_dict = {
    "response": {
        "status": "good",
        "last_updated": "2014-02-16T23:10:12Z",
    }
}
print(xmltodict.unparse(my_dict))
# <?xml version="1.0" encoding="utf-8"?>
# <response><status>good</status><last_updated>2014-02-16T23:10:12Z</last_updated></response>

print()

print(xmltodict.unparse(my_dict, pretty=True))
# <?xml version="1.0" encoding="utf-8"?>
# <response>
# 	<status>good</status>
# 	<last_updated>2014-02-16T23:10:12Z</last_updated>
# </response>

print("\n")

# Text values for nodes can be specified with the cdata_key key in the python dict, while node properties can
# be specified with the attr_prefix prefixed to the key name in the python dict. The default value for attr_
# prefix is @ and the default value for cdata_key is #text.
my_dict = {
    "text": {
        "@color": "red",
        "@stroke": "2",
        "#text": "This is a test",
    }
}
print(xmltodict.unparse(my_dict, pretty=True))
# <?xml version="1.0" encoding="utf-8"?>
# <text stroke="2" color="red">This is a test</text>
