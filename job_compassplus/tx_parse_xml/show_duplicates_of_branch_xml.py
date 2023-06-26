#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup


def get_duplicates(project_dir: str | Path) -> dict[str, int]:
    if isinstance(project_dir, str):
        project_dir = Path(project_dir)

    file_name_branch = project_dir / "branch.xml"

    with open(file_name_branch, encoding="utf-8") as f:
        root = BeautifulSoup(f, "html.parser")

    items = []
    for module in root.select("moduleinfo"):
        layer_url = module.layerurl.text
        module_id = module.moduleid.text
        name = f"{layer_url}-{module_id}"

        definition_path = None
        if module.definition:
            definition_path = module.definition.get("path")

        if definition_path and definition_path != module_id:
            name += f': {module.definition["path"]}'

        items.append(name)

    return {name: number for name, number in Counter(items).items() if number > 1}


if __name__ == "__main__":
    project_dir = "C:/DEV__TX/trunk_tx"
    duplicates = get_duplicates(project_dir)

    for name, number in sorted(duplicates.items(), reverse=True):
        print(f"{name} = {number}")
