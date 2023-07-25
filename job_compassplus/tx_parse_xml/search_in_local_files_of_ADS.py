#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
import xml.etree.ElementTree as ET

from pathlib import Path


NS = dict(
    ads="http://schemas.radixware.org/adsdef.xsd",
)


def get_text(el: ET.Element) -> str:
    if el is None:
        return ""
    return "".join(text for text in el.itertext())


def process(path: str, regexp: str):
    pattern = re.compile(regexp)

    for p in Path(path).glob("*/ads/*/locale/*/mlb*.xml"):
        mlb = ET.fromstring(p.read_bytes())

        for string_el in mlb.findall(".//ads:String", namespaces=NS):
            string_value_el = string_el.find("./ads:Value", namespaces=NS)
            string_value = get_text(string_value_el)

            if pattern.search(string_value):
                string_id = string_el.attrib["Id"]
                string_lang = string_value_el.attrib["Language"]

                print(f"Found with id={string_id} language={string_lang}: {string_value!r}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Search in locale"
    )
    parser.add_argument(
        "path_trunk",
        metavar="/PATH/TO/TRUNK",
        help="Path to TX source tree (the directory containing branch.xml)",
    )
    parser.add_argument(
        "regexp",
        help="Regular expression",
    )
    args = parser.parse_args()

    process(args.path_trunk, args.regexp)
