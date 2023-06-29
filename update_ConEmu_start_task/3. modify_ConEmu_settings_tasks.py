#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as dt
import xml.etree.ElementTree as ET
import sys

sys.path.append(r"../XML/xml.etree.ElementTree__examples")
from pretty_print import indent

from config import FILE_NAME_CONEMU_SETTINGS
from common import (
    PATTERN_CONEMU_TASK,
    PATTERN_FILE_TASK,
    fill_string_pattern,
    get_gist_files,
)


def get_current_datetime() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def update_tasks(tasks_el: ET.Element):
    tasks_el.attrib["modified"] = get_current_datetime()

    tasks = tasks_el.findall("key")

    tasks_count_el = tasks_el.find('value[@name="Count"]')
    tasks_count_el.attrib["data"] = str(len(tasks))

    for i, task_el in enumerate(tasks, 1):
        task_el.attrib["name"] = f"Task{i}"
        task_el.attrib["modified"] = tasks_el.attrib["modified"]
        task_el.attrib["build"] = tasks_el.attrib["build"]


def create_task(tasks_el: ET.Element, name: str, commands: list[str]):
    task_el = ET.SubElement(tasks_el, "key")

    ET.SubElement(task_el, "value", name="Name", type="string", data="{%s}" % name)
    ET.SubElement(task_el, "value", name="Flags", type="dword", data="00000004")
    ET.SubElement(task_el, "value", name="Hotkey", type="dword", data="00000000")
    ET.SubElement(task_el, "value", name="GuiArgs", type="string", data="")
    ET.SubElement(task_el, "value", name="Active", type="long", data="0")
    ET.SubElement(task_el, "value", name="Count", type="long", data=f"{len(commands)}")

    for i, cmd in enumerate(commands, 1):
        ET.SubElement(task_el, "value", name=f"Cmd{i}", type="string", data=cmd)


tree = ET.parse(FILE_NAME_CONEMU_SETTINGS)
root = tree.getroot()

tasks_el = root.find('.//key[@name="Tasks"]')

# Удаление старых задач
for task_el in tasks_el.findall("key[@name]"):
    name = task_el.find('value[@name="Name"]').attrib["data"]
    if PATTERN_CONEMU_TASK.search(name):
        tasks_el.remove(task_el)

# Добавление новых задач
for file_name in get_gist_files():
    m = PATTERN_FILE_TASK.search(file_name.stem)
    if not m:
        continue

    lines = file_name.read_text("utf-8").splitlines()
    lines = list(filter(None, lines))  # Remove empty lines

    task_name = fill_string_pattern(PATTERN_CONEMU_TASK, m.group(1))
    create_task(tasks_el, task_name, lines)

# Актуализация счетчика задач
update_tasks(tasks_el)

indent(root)

tree.write(FILE_NAME_CONEMU_SETTINGS)
