#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from common import RegistryKey


PATHS = [
    r"HKCU\Software\Microsoft\Windows\CurrentVersion\Group Policy\Scripts",
    r"HKLM\Software\Microsoft\Windows\CurrentVersion\Group Policy\Scripts",
    r"HKCU\Software\Policies\Microsoft\Windows\System\Scripts",
    r"HKLM\Software\Policies\Microsoft\Windows\System\Scripts",
]


def get_scripts() -> dict[str, str]:
    path_by_value = dict()

    for path in PATHS:
        key = RegistryKey.get_or_none(path)
        if not key:
            continue

        # Example: <path>\Logon
        for key_type in key.subkeys():
            # Example: <path>\Logon\0
            for key_group in key_type.subkeys():
                file_sys_path = key_group.get_str_value("FileSysPath")

                # Example: <path>\Logon\0\0
                for key_script in key_group.subkeys():
                    script = key_script.get_str_value("Script")
                    parameters = key_script.get_str_value("Parameters")
                    value = f"FileSysPath={file_sys_path}, Script={script}, Parameters={parameters}"

                    path_by_value[key_script.path] = value

    return path_by_value


if __name__ == "__main__":
    for path, value in get_scripts().items():
        print(path, value)
    # HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Group Policy\Scripts\Logon\0\0 FileSysPath=\\...\User, Script=domain.bat, Parameters=
    # HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Group Policy\Scripts\Logon\1\0 FileSysPath=\\...\User, Script=start.bat, Parameters=
