#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import shutil
import sys
from pathlib import Path

sys.path.append("..")
from tx_parse_xml.get_layer_version import get_layer_version


# Example: org.radixware\kernel\common\bin
KERNEL_COMMON_BIN_JARS: list[str] = [
    "xb_acs.jar",
    "xb_adsdef.jar",
    "xb_commondef.jar",
    "xb_utils.jar",
    "general.jar",
    "xb_msdl.jar",
    "xb_types.jar",
]

# Example: org.radixware\kernel\common\lib
KERNEL_COMMON_LIB_JARS: list[str] = [
    "log4j-api-2.17.1.jar",
    "log4j-core-2.17.1.jar",
    "saxon-HE-10.3.jar",
    "xbean.jar",
    "xbean_xpath.jar",
    "xercesImpl-2.9.1.jar",
]

OTHER_PATHS: dict[str, str] = {
    "ads/ServiceBus/bin/common.jar": "ServiceBus-common.jar",
}


def process(root_dir: Path):
    path_radix = root_dir / "org.radixware"
    if not path_radix.exists():
        raise Exception(f'Not found path {str(path_radix)!r}!')

    radix_version = get_layer_version(path_radix)
    print("Radix version:", radix_version)

    # NOTE: Текущая папка скрипта
    path_to_copy = Path(__file__).resolve().parent / f"radix-{radix_version}"

    path_kernel_common_bin = path_radix / "kernel/common/bin"
    if not path_kernel_common_bin.exists():
        raise Exception(f'Not found path {str(path_kernel_common_bin)!r}!')

    path_kernel_common_lib = path_radix / "kernel/common/lib"
    if not path_kernel_common_lib.exists():
        raise Exception(f'Not found path {str(path_kernel_common_lib)!r}!')

    old_to_new_paths: dict[Path, Path] = dict()

    for file in KERNEL_COMMON_BIN_JARS:
        old_path = path_kernel_common_bin / file
        old_to_new_paths[old_path] = path_to_copy / old_path.name

    for file in KERNEL_COMMON_LIB_JARS:
        old_path = path_kernel_common_lib / file
        old_to_new_paths[old_path] = path_to_copy / old_path.name

    for file, new_file in OTHER_PATHS.items():
        old_path = path_radix / file
        old_to_new_paths[old_path] = path_to_copy / new_file

    # Проверка наличия всех путей
    for old_path in old_to_new_paths.keys():
        if not old_path.exists():
            raise Exception(f'Not found path {str(old_path)!r}!')

    path_to_copy.mkdir(exist_ok=True, parents=True)
    for old_path, new_path in old_to_new_paths.items():
        print(f"Copy {str(old_path)!r} to {str(new_path)!r}")
        shutil.copy(old_path, new_path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Copying jar from radix"
    )
    parser.add_argument(
        "root_path",
        metavar="/PATH/TO/PROJECT",
        type=Path,
        help="Path to source tree (the directory containing branch.xml)",
    )
    args = parser.parse_args()

    process(args.root_path)
