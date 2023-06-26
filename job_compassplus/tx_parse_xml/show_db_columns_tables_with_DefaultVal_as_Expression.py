#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import xml.etree.ElementTree as ET

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Column:
    id: str
    name: str
    default_value: str


def get_table_by_columns(model_path: Path) -> dict[str, list[Column]]:
    ns = dict(
        dds="http://schemas.radixware.org/ddsdef.xsd",
        com="http://schemas.radixware.org/commondef.xsd",
    )

    table_by_columns = defaultdict(list)
    model = ET.fromstring(model_path.read_text(encoding="utf-8"))
    for table in model.findall(".//dds:Tables/dds:Table", namespaces=ns):
        table_title = f"{table.attrib['Name']}({table.attrib['Id']})"

        for column in table.findall("./dds:Columns/dds:Column", namespaces=ns):
            default_value = column.find(
                "./dds:DefaultVal[@Type='Expression']/com:Value", namespaces=ns
            )
            if default_value is not None:
                table_by_columns[table_title].append(
                    Column(
                        id=column.attrib["Id"],
                        name=column.attrib["Name"],
                        default_value=default_value.text.strip(),
                    )
                )

    return table_by_columns


def process(branch_dir: Path | str) -> dict[str, dict[str, list[Column]]]:
    if isinstance(branch_dir, str):
        branch_dir = Path(branch_dir)

    layer_module_by_tables = defaultdict(dict)

    for layer_dir in branch_dir.glob("*"):
        if not layer_dir.is_dir():
            continue

        layer_dds_dir = layer_dir / "dds"
        if layer_dds_dir.is_dir():
            layer = layer_dir.name
            for model_xml in layer_dds_dir.glob("*/model.xml"):
                module = model_xml.parent.name

                for table, columns in get_table_by_columns(model_xml).items():
                    key = f"{layer}/{module}"
                    layer_module_by_tables[key][table] = columns

    return layer_module_by_tables


if __name__ == "__main__":
    path = r"C:\DEV__OPTT\trunk_optt"

    for key, table_by_columns in process(path).items():
        print(f"{key} ({len(table_by_columns)})")
        for i, (table, columns) in enumerate(table_by_columns.items(), 1):
            print(f"    {i}. {table}:")
            for column in columns:
                print(f"        {column.name}({column.id}) = {column.default_value!r}")
        print()
    """
    com.optt/ProtocolSetup (7)
        1. Protocol(tblJBLJOL4TFBAHLBEWZMLSHXYGMM):
            extGuid(colW44QAAJJP5ELXOLWL5KKHTLUKI) = 'sys_guid()'
        2. ProtocolField(tblE26CRSMVJZCJVF4ZMR56KUYTAM):
            extGuid(colRO63O6OLMRBSNJRIBSSV3HRVOQ) = 'sys_guid()'
        3. ProtocolStateAttribute(tblFP3C5RQFDFFWJAJQMYVXSQ3SEY):
            extGuid(col3MK2X5H3ZZBVVJB3AYDMMDCWHQ) = 'sys_guid()'
        4. MessageType(tbl2DX3TB7ZUZE4RG3B7BY6HS4EZI):
            extGuid(col73V3MXLEKFD4BASZ2JXAEB4X4A) = 'sys_guid()'
        5. Rule(tblE4HU6SKERVDMHJBSB4D6SCPUVQ):
            extGuid(colAN5WEW42GBATLDBNPREXMUY5PU) = 'sys_guid()'
        6. FieldValueGenerator(tblGU3P5FK7PZD4VLOS4XR5236L6Q):
            extGuid(colBDVB7VL5ARAVRLSYA2J5YEMBFU) = 'sys_guid()'
        7. ProtocolVersion(tblQLF47J7P4JCY5E6JFJ62NJBTRQ):
            extGuid(colJLFFQTXRX5FFJG6AG3AL4MFNDM) = 'sys_guid()'
    """
