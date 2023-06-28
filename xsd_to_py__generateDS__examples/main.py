#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: http://www.davekuhlman.org/generateDS.html
# pip install generateDS


from pathlib import Path

# Generate from generate_py_from_xsd.cmd
import task


dir_tasks = Path(r"C:\Windows\System32\Tasks")
files = [f for f in dir_tasks.rglob("*") if f.is_file()]
for f in files:
    print(f)
    task_obj = task.parse(f, silence=True)
    actions = []
    actions += task_obj.Actions.Exec
    actions += task_obj.Actions.ComHandler
    actions += task_obj.Actions.SendEmail
    actions += task_obj.Actions.ShowMessage

    print(f"    URI: {task_obj.RegistrationInfo.URI}")
    print(f"    Enabled: {task_obj.Settings.Enabled}")
    print(f"    Actions ({len(actions)}):", actions)
    print()
