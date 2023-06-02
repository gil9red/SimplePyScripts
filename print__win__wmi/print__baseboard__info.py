#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import xml.etree.ElementTree as ET
from subprocess import check_output


def get_baseboard_info() -> dict:
    # Motherboard model
    cmd = "wmic baseboard get product, Manufacturer, version, serialnumber /format:RAWXML"
    text = check_output(cmd)

    root = ET.fromstring(text)

    result = dict()
    for x in root.iter("PROPERTY"):
        key = x.attrib["NAME"]
        result[key] = x.find("VALUE").text

    return result


if __name__ == "__main__":
    info = get_baseboard_info()
    print(info)
    print(info["Product"])
