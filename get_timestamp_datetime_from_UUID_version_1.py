#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import uuid
from datetime import datetime as DT


# SOURCE: https://stackoverflow.com/a/3795750/5909792


uuid_variant1_list = [
    "a860729c-c7c0-11e8-94e9-f079598c1eec", "a8f9c0dc-c7c0-11e8-84fc-f079598c1eec",
    "a9925f02-c7c0-11e8-8a15-f079598c1eec", "aa2b2152-c7c0-11e8-90a0-f079598c1eec"
]

for uuid1_value in uuid_variant1_list:
    uuid_1 = uuid.UUID(uuid1_value)
    timestamp = (uuid_1.time - 0x01b21dd213814000) * 100 / 1e9
    print("'{}': {} -> {}".format(uuid_1, timestamp, DT.fromtimestamp(timestamp)))
