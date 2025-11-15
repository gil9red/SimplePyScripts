#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
import subprocess

from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Optional, Any


def get_diff_fields(obj1, obj2) -> dict[str, tuple[Any, Any]]:
    """
    Compares two dataclass instances and returns a dictionary of differing fields.
    The dictionary keys are the field names, and values are a tuple
    (value_in_obj1, value_in_obj2).
    """

    if not isinstance(obj1, type(obj2)):
        raise TypeError("Both objects must be instances of the same dataclass.")

    diffs: dict[str, tuple[Any, Any]] = dict()
    for field_info in fields(obj1):
        field_name: str = field_info.name
        value1: Any = getattr(obj1, field_name)
        value2: Any = getattr(obj2, field_name)

        if value1 != value2:
            diffs[field_name] = value1, value2

    return diffs


def parse_xml_attrs(text: str) -> dict[str, str]:
    return dict(re.findall(r'(\w+)\s*=\s*"(.+?)"', text))


def parse_line_xml_text(text: str, line_contains: list[str]) -> dict[str, str]:
    for line in text.splitlines():
        if all(x in line for x in line_contains):
            return parse_xml_attrs(line)

    return dict()


def get_remote_file_from_svn(file_name: Path) -> str:
    try:
        result: bytes = subprocess.check_output(
            args=["svn", "info", file_name],
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as e:
        # NOTE: svn: warning: W155010: The node 'xxx' was not found.
        if b"W155010" in e.stderr:
            print(f"[#] Не найден {file_name} в SVN")
            return ""

        raise e

    url_svn_file: str | None = None
    for line in result.splitlines():
        parts: list[bytes] = line.split(b"URL:", maxsplit=1)
        if len(parts) < 2:
            continue

        url_svn_file = parts[1].strip().decode("ascii")
        break

    if not url_svn_file:
        raise Exception(
            f"Не удалось получить URL файла {file_name} в репозитории SVN из результата svn info:\n{result!r}"
        )

    return subprocess.check_output(
        args=["svn", "cat", url_svn_file],
        encoding="utf-8",
    )


@dataclass
class BranchInfo:
    # TODO: Не все поля были поддержаны
    base_dev_uri: str
    type: str
    base_release: str | None
    last_release: str | None

    @classmethod
    def parse_from_dict(cls, d: dict[str, str]) -> "BranchInfo":
        return cls(
            base_dev_uri=d["BaseDevUri"],
            type=d["Type"],
            base_release=d.get("BaseRelease"),
            last_release=d.get("LastRelease"),
        )

    @classmethod
    def parse_from_text(cls, text: str) -> Optional["BranchInfo"]:
        xml_attrs: dict[str, str] = parse_line_xml_text(
            text=text,
            line_contains=["Branch", "BaseDevUri", "Type"],
        )
        if xml_attrs:
            return cls.parse_from_dict(xml_attrs)


@dataclass
class LayerInfo:
    # TODO: Не все поля были поддержаны
    uri: str
    name: str
    release_number: str | None
    base_layer_uris: list[str] = field(default_factory=list)

    @classmethod
    def parse_from_dict(cls, d: dict[str, str]) -> "LayerInfo":
        return cls(
            uri=d["Uri"],
            name=d["Name"],
            release_number=d.get("ReleaseNumber"),
            base_layer_uris=d.get("BaseLayerURIs", "").split(),
        )

    @classmethod
    def parse_from_text(cls, text: str) -> Optional["LayerInfo"]:
        xml_attrs: dict[str, str] = parse_line_xml_text(
            text=text,
            line_contains=["Layer", "Uri", "Name"],
        )
        if xml_attrs:
            return cls.parse_from_dict(xml_attrs)


@dataclass
class ProjectInfo:
    branch: BranchInfo | None
    layers: list[LayerInfo]


@dataclass
class TotalProjectInfo:
    local: ProjectInfo
    remote: ProjectInfo


def collect_all_layer_infos(
    path_layer: Path,
    layer_infos: list[LayerInfo],
    remote: bool = False,
):
    if not path_layer.exists():
        raise Exception(f"Путь {path_layer} не существует!")

    layer_info: LayerInfo | None = LayerInfo.parse_from_text(
        get_remote_file_from_svn(path_layer)
        if remote
        else path_layer.read_text(encoding="utf-8")
    )

    if not layer_info:
        text = f"Не удалось получить информацию из {path_layer}!"
        if not remote:
            raise Exception(f"{text} (local)")

        print(f"[#] {text} (remote)")
        return

    if layer_info in layer_infos:
        print(f"[#] Обнаружилось зацикливание с {layer_info}")
        return

    layer_infos.append(layer_info)

    if not layer_info.base_layer_uris:
        return

    for base_layer_uri in layer_info.base_layer_uris:
        path_layer = path_layer.parent.parent / base_layer_uri / "layer.xml"
        collect_all_layer_infos(path_layer, layer_infos, remote=remote)


def get_project_versions(path: Path) -> TotalProjectInfo:
    path = path.resolve()

    if not path.is_dir():
        raise Exception(f"Путь {path} должен быть директорией")

    path_branch = path / "branch.xml"
    if not path_branch.exists():
        raise Exception(f"Не существует: {path_branch}")

    branch_info_local: BranchInfo | None = BranchInfo.parse_from_text(
        path_branch.read_text(encoding="utf-8")
    )
    if not branch_info_local:
        raise Exception(
            f"Не удалось получить информацию из {branch_info_local}! (local)"
        )

    branch_info_remote: BranchInfo | None = BranchInfo.parse_from_text(
        get_remote_file_from_svn(path_branch)
    )
    if not branch_info_remote:
        print(f"[#] Не удалось получить информацию из {branch_info_remote}! (remote)")

    path_base_dev_layer = path / branch_info_local.base_dev_uri / "layer.xml"

    layer_infos_local: list[LayerInfo] = []
    collect_all_layer_infos(path_base_dev_layer, layer_infos_local, remote=False)

    layer_infos_remote: list[LayerInfo] = []
    collect_all_layer_infos(path_base_dev_layer, layer_infos_remote, remote=True)

    return TotalProjectInfo(
        local=ProjectInfo(
            branch=branch_info_local,
            layers=layer_infos_local,
        ),
        remote=ProjectInfo(
            branch=branch_info_remote,
            layers=layer_infos_remote,
        ),
    )


def process(path: Path):
    print(f"Информация по версиям из {path}")

    total_project_info: TotalProjectInfo = get_project_versions(path)

    if not total_project_info.local.branch:
        print()
        print("[#] Local branch: <нет информации>")
    elif not total_project_info.remote.branch:
        print()
        print("[#] Remote branch: <нет информации>")
    else:
        diff_branches: dict[str, tuple[Any, Any]] = get_diff_fields(
            total_project_info.local.branch, total_project_info.remote.branch
        )
        if diff_branches:
            print()

            print("Обнаружена разница в полях Branch между local и remote:")
            for field_name, (value_local, value_remote) in diff_branches.items():
                print(f"    {field_name}: {value_local} != {value_remote}")

    @dataclass
    class DiffLayersResult:
        local: LayerInfo | None = None
        remote: LayerInfo | None = None

    uri_by_layers: dict[str, DiffLayersResult] = {
        uri: DiffLayersResult()
        for uri in set(
            l.uri
            for l in (
                total_project_info.local.layers + total_project_info.remote.layers
            )
        )
    }

    for l in total_project_info.local.layers:
        uri_by_layers[l.uri].local = l
    for l in total_project_info.remote.layers:
        uri_by_layers[l.uri].remote = l

    diff_layers_local: list[LayerInfo] = []
    diff_layers_remote: list[LayerInfo] = []
    for uri, layers in uri_by_layers.items():
        if layers.local and layers.remote:
            diff_layers: dict[str, tuple[Any, Any]] = get_diff_fields(
                layers.local, layers.remote
            )
            if diff_layers:
                print()
                print(f"Обнаружена разница в полях Layer ({uri}) между local и remote:")
                for field_name, (value_local, value_remote) in diff_layers.items():
                    print(f"    {field_name}: {value_local} != {value_remote}")

        elif layers.local:
            diff_layers_remote.append(layers.local)
        elif layers.remote:
            diff_layers_local.append(layers.remote)

    if diff_layers_local:
        print()
        print(f"В Local нет слоев из Remote ({len(diff_layers_local)}):")
        for l in diff_layers_local:
            print(f"    {l}")

    if diff_layers_remote:
        print()
        print(f"В Local нет слоев из Remote ({len(diff_layers_remote)}):")
        for l in diff_layers_remote:
            print(f"    {l}")

    print()
    print("Версии:")

    def _print_project_info(project_info: ProjectInfo, is_local: bool):
        ind1: str = "    "
        print(ind1 + ("Local:" if is_local else "Remote:"))
        print(f"{ind1 * 2}Branch: {project_info.branch}")
        print(f"{ind1 * 2}Layers:")
        for layer in project_info.layers:
            print(f"{ind1 * 3}{layer}")

    _print_project_info(total_project_info.local, is_local=True)
    print()
    _print_project_info(total_project_info.remote, is_local=False)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Print a layer version")
    parser.add_argument(
        "path",
        metavar="/PATH/TO/PROJECT",
        type=Path,
        help="Path to project (the directory containing branch.xml)",
    )
    args = parser.parse_args()

    process(args.path)
