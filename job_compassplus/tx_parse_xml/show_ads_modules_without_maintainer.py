#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import xml.etree.ElementTree as ET
from pathlib import Path


def get_module_ids_with_maintainter(path_branch: str | Path) -> list[str]:
    ns = dict(
        p="http://schemas.radixware.org/product.xsd",
    )

    ids: list[str] = []

    branch = ET.fromstring(path_branch.read_bytes())
    for module_info_el in branch.findall(".//p:ModuleInfo", namespaces=ns):
        module_id = module_info_el.find("./p:ModuleId", namespaces=ns).text
        has_maintainters = module_info_el.find(".//p:OwnerEmail", namespaces=ns) is not None
        if has_maintainters and module_id not in ids:
            ids.append(module_id)

    return ids


def process(path_layer: str):
    if isinstance(path_layer, str):
        path_layer = Path(path_layer)

    if not path_layer.exists():
        raise Exception(f"Not exists: {path_layer}")

    path_branch = path_layer.parent / "branch.xml"
    if not path_branch.exists():
        raise Exception(f"Not exists: {path_branch}")

    module_ids: list[str] = get_module_ids_with_maintainter(path_branch)

    deprecated_module_without_maintainters: list[tuple[str, str]] = []
    module_without_maintainters: list[tuple[str, str]] = []

    for path_module in path_layer.glob("ads/*/module.xml"):
        module_name = path_module.parent.name

        module_el = ET.fromstring(path_module.read_bytes())
        module_id = module_el.get("Id")
        if module_id in module_ids:
            continue

        is_deprecated = module_el.get("IsDeprecated") == "true"
        if is_deprecated:
            deprecated_module_without_maintainters.append((module_name, module_id))
        else:
            module_without_maintainters.append((module_name, module_id))

    print(f"Modules without maintainters ({len(module_without_maintainters)}):")
    for module_name, module_id in module_without_maintainters:
        print(f"    {module_name} ({module_id})")

    print()

    print(f"Deprecated modules without maintainters ({len(deprecated_module_without_maintainters)}):")
    for module_name, module_id in deprecated_module_without_maintainters:
        print(f"    {module_name} ({module_id})")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Show ads modules without maintainer"
    )
    parser.add_argument(
        "path_layer",
        metavar="/PATH/TO/TRUNK/LAYER",
        help="Path to layer (the directory containing layer.xml)",
    )
    args = parser.parse_args()

    process(args.path_layer)
