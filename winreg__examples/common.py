#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as dt
import winreg

from typing import Optional, Any
from pathlib import Path
from winreg import (
    QueryInfoKey,
    EnumKey,
    EnumValue,
    OpenKey,
    HKEYType,
    REG_EXPAND_SZ,
    ExpandEnvironmentStrings,
)

from exceptions import RegistryKeyNotFoundException, RegistryValueNotFoundException
from constants import VALUE_BY_TYPE


def expand_registry_key(key: str) -> str:
    return {
        "HKCR": "HKEY_CLASSES_ROOT",
        "HKCU": "HKEY_CURRENT_USER",
        "HKLM": "HKEY_LOCAL_MACHINE",
        "HCU": "HKEY_USERS",
    }.get(key, key)


def expand_path(path: str) -> str:
    registry_key_name, relative_path = path.split("\\", maxsplit=1)
    registry_key_name = expand_registry_key(registry_key_name)

    return rf"{registry_key_name}\{relative_path}"


def get_key(path: str) -> Optional[HKEYType]:
    # Example:
    #     path = r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
    #     registry_key_name = "HKEY_LOCAL_MACHINE"
    #     relative_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
    registry_key_name, relative_path = path.split("\\", maxsplit=1)
    registry_key_name = expand_registry_key(registry_key_name)

    registry_key = getattr(winreg, registry_key_name)

    try:
        return OpenKey(registry_key, relative_path)
    except:
        return


class RegistryValue:
    def __init__(self, name: str, value_type: int, value: Any) -> None:
        self.name: str = name

        self.value_type: int = value_type
        self.value_type_str: str = VALUE_BY_TYPE[value_type]

        if self.value_type == REG_EXPAND_SZ:
            value = ExpandEnvironmentStrings(value)

        self.value: Any = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', type={self.value_type_str}, value={self.value})"


class RegistryKey:
    def __init__(self, path: str) -> None:
        path = expand_path(path)

        self.hkey: HKEYType = get_key(path)
        if not self.hkey:
            raise RegistryKeyNotFoundException(path)

        self.path: str = path
        self.name: str = path.split("\\")[-1]

        number_of_keys, number_of_values, last_modified_timestamp = QueryInfoKey(
            self.hkey
        )
        self.number_of_keys: int = number_of_keys
        self.number_of_values: int = number_of_values
        self.last_modified_timestamp: int = last_modified_timestamp

        delta = dt.timedelta(seconds=self.last_modified_timestamp / 1e7)
        self.last_modified: dt.datetime = dt.datetime(1601, 1, 1) + delta

    def __getitem__(self, name: str) -> RegistryValue:
        return self.value(name)

    def __truediv__(self, sub_key_name: str) -> "RegistryKey":
        return self.subkey(sub_key_name)

    def __eq__(self, other: "RegistryKey") -> bool:
        return hash(self.path) == hash(other.path)

    def __hash__(self) -> int:
        return hash(self.path)

    @classmethod
    def get_subkey(cls, path: str, sub_key_name: str) -> "RegistryKey":
        return cls(rf"{path}\{sub_key_name}")

    @classmethod
    def get_or_none(cls, path: str) -> Optional["RegistryKey"]:
        try:
            return cls(path)
        except RegistryKeyNotFoundException:
            return

    def subkeys(self) -> list["RegistryKey"]:
        items = []
        for i in range(self.number_of_keys):
            sub_key_name = EnumKey(self.hkey, i)
            items.append(RegistryKey.get_subkey(self.path, sub_key_name))
        return items

    def subkey(self, name: str) -> "RegistryKey":
        for k in self.subkeys():
            if k.name.upper() == name.upper():
                return k
        raise RegistryKeyNotFoundException(rf"{path}\{name}")

    def values(self) -> list[RegistryValue]:
        items = []
        for i in range(self.number_of_values):
            name, value, value_type = EnumValue(self.hkey, i)
            items.append(RegistryValue(name=name, value_type=value_type, value=value))
        return items

    def value(self, name: str) -> RegistryValue:
        for v in self.values():
            if v.name.upper() == name.upper():
                return v
        raise RegistryValueNotFoundException(self.path, name)

    def get_raw_value(self, name: str, default: Any = None) -> Any:
        try:
            return self.value(name).value
        except RegistryValueNotFoundException:
            return default

    def get_str_value(self, name: str, default: str = "") -> str:
        return str(self.get_raw_value(name, default))

    def get_path_value(self, name: str) -> Optional[Path]:
        path = self.get_str_value(name)
        if not path:
            return

        return Path(path)

    def get_raw_values_as_dict(self, default: Any = None) -> dict[str, Any]:
        return {v.name: v.value if v.value else default for v in self.values()}

    def get_str_values_as_dict(self, default: str = "") -> dict[str, str]:
        return {
            name: str(value) if value else default
            for name, value in self.get_raw_values_as_dict().items()
        }

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(path='{self.path}', "
            f"number_of_keys={self.number_of_keys}, number_of_values={self.number_of_values})"
        )


if __name__ == "__main__":
    assert get_key(
        r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
    )
    assert get_key(
        r"HKLM\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
    )

    assert get_key(
        r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
    )
    assert get_key(
        r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
    )

    assert (
        expand_path(r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run")
        == r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run"
    )

    path = r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
    key = RegistryKey(path)
    print(key == RegistryKey(path))
    print(hash(key))
    print(hash(RegistryKey(path)))
    print({key: "111"})
    print(key)
    print(key.path)  # TODO: добавить проверку
    print(key.name)  # TODO: добавить проверку
    print(key.hkey)
    print(key.number_of_keys)
    print(key.number_of_values)
    print(key.last_modified_timestamp)
    print(key.last_modified)
    print(len(key.subkeys()), key.subkeys())
    print(len(key.values()), key.values())
    print(key.value("Common Programs"))
    print(key["Common Programs"])
    print(key.subkey("Backup"))
    print(key / "Backup")
    print(key.subkey("BACKUP"))
    print(key.value("COMMON PROGRAMS"))

    # TODO: catch exception, use uuid
    # print(key.subkey('111'))
    # print(key / '111')
    # print(key.value('111'))
    # print(key['111'])
