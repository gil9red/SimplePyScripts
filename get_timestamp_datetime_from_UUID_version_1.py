#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import uuid
from datetime import datetime


# SOURCE: https://stackoverflow.com/a/3795750/5909792


def get_timestamp_from_UUIDv1(uuid_obj: uuid.UUID) -> float:
    return (uuid_obj.time - 0x01B21DD213814000) * 100 / 1e9


def get_datetime_from_UUIDv1(uuid_obj: uuid.UUID) -> datetime:
    timestamp = get_timestamp_from_UUIDv1(uuid_obj)
    return datetime.fromtimestamp(timestamp)


if __name__ == "__main__":
    uuid_obj = uuid.UUID("a860729c-c7c0-11e8-94e9-f079598c1eec")
    print(get_datetime_from_UUIDv1(uuid_obj))  # 2018-10-04 15:31:30.734147
    print()

    uuid_variant1_list = [
        "a860729c-c7c0-11e8-94e9-f079598c1eec",
        "a8f9c0dc-c7c0-11e8-84fc-f079598c1eec",
        "a9925f02-c7c0-11e8-8a15-f079598c1eec",
        "aa2b2152-c7c0-11e8-90a0-f079598c1eec",
    ]

    for uuid1_value in uuid_variant1_list:
        uuid_obj = uuid.UUID(uuid1_value)
        timestamp = get_timestamp_from_UUIDv1(uuid_obj)
        print(
            "'{}': {} -> {}".format(
                uuid_obj, timestamp, datetime.fromtimestamp(timestamp)
            )
        )
