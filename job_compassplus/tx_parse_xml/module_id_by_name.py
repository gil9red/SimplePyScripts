#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path
from show_maintainers import parse_xml_partially


def get_module_id_by_name(project_dir: str | Path) -> dict[str, str]:
    if isinstance(project_dir, str):
        project_dir = Path(project_dir)

    module_id_by_name: dict[str, str] = dict()
    for layer_path in project_dir.glob("*/layer.xml"):
        for path in layer_path.parent.glob("ads/*/module.xml"):
            root_module = parse_xml_partially(
                path, line_contains=["Module ", " Id", " Name"]
            )
            module_id = root_module.module["id"]
            if module_id not in module_id_by_name:
                module_id_by_name[module_id] = root_module.module["name"]

    return module_id_by_name


if __name__ == "__main__":
    project_dir = "C:/DEV__TX/trunk"
    owner_by_modules = get_module_id_by_name(project_dir)

    for module_id, module_name in owner_by_modules.items():
        print(f"{module_id} = {module_name}")
