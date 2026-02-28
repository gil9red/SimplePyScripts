#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from typing import Any, Callable


def walk_dict(
    node: dict,
    value_process_func: Callable[[Any, Any], Any] | None = None,
) -> None:
    for key, value in node.items():
        if value_process_func:
            value = value_process_func(key, value)
            node[key] = value

        if isinstance(value, dict):
            walk_dict(value, value_process_func)


if __name__ == "__main__":
    __SETTINGS = {
        "__radix_base": {
            "options": {
                "version": "AvailabilityEnum.OPTIONAL",
                "what": "AvailabilityEnum.REQUIRED",
                "args": "AvailabilityEnum.OPTIONAL",
                "default_version": "trunk",
            },
            "whats": {
                "compile": "!build_ads__pause.bat",
                "build": "!build_kernel__pause.cmd",
                "update": (
                    "svn update",
                    "${_svn_update}",
                ),
                "log": (
                    "svn log",
                    r'start /b "" TortoiseProc /command:log /path:"{path}" /findstring:"{find_string}"',
                ),
            },
        },
        "radix": {
            "base": "__radix_base",
            "path": "C:/DEV__RADIX",
            "base_version": "2.1.",
        },
    }

    def foo(k: Any, v: Any) -> Any:
        print(k, v)
        return v

    walk_dict(__SETTINGS, value_process_func=foo)
