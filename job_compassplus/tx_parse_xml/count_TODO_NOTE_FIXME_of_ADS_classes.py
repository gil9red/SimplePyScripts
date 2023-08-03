#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import xml.etree.ElementTree as ET

from collections import defaultdict
from pathlib import Path


NS = dict(
    xsc="http://schemas.radixware.org/xscml.xsd",
)


def process(path: str):
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise Exception(f"Not exists: {path}")

    assignee_by_number: dict[str, int] = defaultdict(int)
    type_by_number: dict[str, int] = defaultdict(int)

    for layer_dir in path.glob("*"):
        if not layer_dir.is_dir():
            continue

        layer_ads_dir = layer_dir / "ads"
        if not layer_ads_dir.is_dir():
            continue

        for class_path in layer_ads_dir.glob("*/src/*.xml"):
            model = ET.fromstring(class_path.read_bytes())
            for task_el in model.findall(".//xsc:Task", namespaces=NS):
                assignee = task_el.attrib["Assignee"].strip()
                if not assignee:
                    assignee = "<unknown>"

                assignee_by_number[assignee] += 1

                task_type = task_el.attrib["Type"]
                type_by_number[task_type] += 1

    indent1 = "    "

    print("Total:", sum(assignee_by_number.values()))
    print()

    print(f"assignee_by_number ({len(assignee_by_number)}):")
    for assignee, number in sorted(
        assignee_by_number.items(), key=lambda x: x[1], reverse=True
    ):
        print(f"{indent1}{assignee}: {number}")
    print()

    print(f"type_by_number ({len(type_by_number)}):")
    for task_type, number in sorted(
        type_by_number.items(), key=lambda x: x[1], reverse=True
    ):
        print(f"{indent1}{task_type}: {number}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Count TODO, NOTE, FIXME of ADS classes.py"
    )
    parser.add_argument(
        "path_trunk",
        metavar="/PATH/TO/TRUNK",
        help="Path to source tree (the directory containing branch.xml)",
    )
    args = parser.parse_args()

    process(args.path_trunk)
