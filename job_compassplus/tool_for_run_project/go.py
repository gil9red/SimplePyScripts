#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import copy
import enum
import os
import shutil
import sys
import re
import traceback

from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import Iterable

import requests

sys.path.append("../..")
from from_ghbdtn import from_ghbdtn

sys.path.append("..")
from kill import kill_servers, kill_explorers, kill_designers, get_processes, is_server, is_explorer, is_designer

sys.path.append("../svn")
from get_last_release_version import get_last_release_version
from search_by_versions import search as search_by_versions
from find_release_version import find_release_version


class AvailabilityEnum(Enum):
    OPTIONAL = auto()
    REQUIRED = auto()
    PROHIBITED = auto()


class GoException(Exception):
    pass


class UnknownNameException(GoException):
    def __init__(self, name: str, supported: Iterable[str]):
        self.name = name
        self.supported = list(sorted(supported))

        super().__init__(f"Unknown name {self.name!r}, supported: {self.supported}")


class UnknownWhatException(GoException):
    def __init__(self, what: str, supported: Iterable[str]):
        self.what = what
        self.supported = list(sorted(supported))

        super().__init__(f"Unknown what {self.what!r}, supported: {self.supported}")


class UnknownVersionException(GoException):
    def __init__(self, version: str, supported: Iterable[str]):
        self.version = version
        self.supported = list(supported)

        super().__init__(
            f"Unknown version {self.version!r}, supported: {self.supported}"
        )


class ParameterMissing(GoException):
    def __init__(self, name: str, param: str):
        self.name = name
        self.param = param

        super().__init__(f"For {self.name!r} the value <{self.param}> must not be set!")


class ParameterAvailabilityException(GoException):
    def __init__(self, command: "Command", param: str, availability: AvailabilityEnum):
        if availability == AvailabilityEnum.REQUIRED:
            post_fix = "должно быть установлено!"
        elif availability == AvailabilityEnum.PROHIBITED:
            post_fix = "не может быть установлено!"
        else:
            raise GoException(f"Не поддерживается: {availability}!")

        self.command = command
        self.param = param
        self.availability = availability

        super().__init__(
            f"Для {self.command.name!r} значение <{self.param}> " + post_fix
        )


class JenkinsJobCheckException(GoException):
    pass


URL_JENKINS = "http://10.77.204.68:8080"


def do_check_jenkins_job(url: str, version: str):
    url = url.format(URL_JENKINS=URL_JENKINS, version=version)

    rs = requests.get(url)
    if rs.status_code == 404:
        raise JenkinsJobCheckException(f"Сборки для версии {version} нет.")

    rs.raise_for_status()

    data = rs.json()

    result = data["result"]
    if not result:
        duration = datetime.now() - datetime.fromtimestamp(data["timestamp"] / 1000)

        # "0:39:56.476184" -> "0:39:56"
        duration_str = str(duration).split(".")[0]

        raise JenkinsJobCheckException(f"Сборка еще в процессе, прошло {duration_str}.")

    if result != "SUCCESS":
        raise JenkinsJobCheckException(f"Сборка поломанная, обновление прервано.")


@dataclass
class Command:
    name: str
    version: str | None = None
    what: str | None = None
    args: list[str] | None = None

    def _check_parameter(self, param: str):
        settings = SETTINGS[self.name]

        value = getattr(self, param)
        settings_param = settings["options"][param]
        if settings_param == AvailabilityEnum.REQUIRED:
            if not value:
                raise ParameterAvailabilityException(self, param, settings_param)

        elif settings_param == AvailabilityEnum.PROHIBITED:
            if value:
                raise ParameterAvailabilityException(self, param, settings_param)

    def run(self):
        settings = SETTINGS[self.name]

        settings_version = settings["options"]["version"]
        if settings_version == AvailabilityEnum.OPTIONAL and not self.version:
            self.version = resolve_version(
                self.name, settings["options"]["default_version"]
            )

        self._check_parameter("version")
        self._check_parameter("what")
        self._check_parameter("args")

        # TODO: Переписать do_run для использования только Command
        go_run(self.name, self.version, self.what, self.args, self)


@dataclass
class RunContext:
    command: Command
    description: str = ""


# SOURCE: https://stackoverflow.com/a/20666342/5909792
def merge_dicts(source: dict, destination: dict) -> dict:
    for key, value in source.items():
        if isinstance(value, dict):
            # Get node or create one
            node = destination.setdefault(key, dict())
            merge_dicts(value, node)
        else:
            destination[key] = value

    return destination


def get_similar_value(alias: str, items: Iterable) -> str | None:
    if alias in items:
        return alias

    # Ищем похожие ключи по начальной строке
    keys = [key for key in items if key.startswith(alias)]

    # Нашли одну вариацию - подходит
    if len(keys) == 1:
        return keys[0]


def has_similar_value(alias: str, items: list) -> bool:
    return get_similar_value(alias, items) is not None


def is_like_a_short_version(value: str) -> bool:
    # Вариант .isdigit() для коротких версий, не 3.2.25, а 25
    return value.isdigit()


def is_like_a_version(value: str) -> bool:
    trunk = "trunk"
    trunk_invert = from_ghbdtn(trunk)  # from_ghbdtn('trunk') = 'екгтл'
    return (
        trunk in value  # Для файлов
        or bool(get_similar_value(value, [trunk, trunk_invert]))
        or bool(re.search(r"\d+(\.\d+)+", value))
        or is_like_a_short_version(value)
        or "-" in value  # Example: "23-25" or "23-trunk"
        or "," in value  # Example: "23,24,25" or "23,24,25,trunk"
    )


def get_settings(name: str) -> dict:
    name = resolve_name(name)
    return SETTINGS[name]


def get_path_by_name(name: str) -> str:
    settings = get_settings(name)
    return settings["path"]


def get_versions_by_path(path: str) -> dict[str, str]:
    version_by_path = dict()

    dir_path = Path(path)

    if dir_path.is_dir():
        for path in dir_path.iterdir():
            if path.is_dir() and is_like_a_version(path.name):
                version_by_path[path.name] = str(path)

    return version_by_path


def settings_preprocess(settings: dict[str, dict]) -> dict[str, dict]:
    new_settings = dict()

    # Update from bases
    for name, values in settings.items():
        if "base" in values:
            # Removing base name
            base_name = values.pop("base")
            base_values = settings[base_name]
            new_settings[name] = copy.deepcopy(base_values)

        if name not in new_settings:
            new_settings[name] = dict()

        merge_dicts(values, new_settings[name])

        if (
            "path" in new_settings[name]
            and new_settings[name]["options"]["version"] != AvailabilityEnum.PROHIBITED
        ):
            path = new_settings[name]["path"]
            new_settings[name]["versions"] = get_versions_by_path(path)

    # Removing private names
    private_names = [name for name in new_settings if name.startswith("__")]
    for name in private_names:
        new_settings.pop(name)

    return new_settings


def _run_path(path: str, args: list[str] | None = None, context: RunContext = None):
    if not args:
        print("Нужно задать маску файла")
        return

    file_mask = args[0]

    files = list(Path(path).glob(file_mask))
    if not files:
        print("Не найден файл")
        return

    if len(files) > 1:
        print(f"Маска файла должна соответствовать одному файлу.\nНайдено ({len(files)}):")
        for name in files:
            print(f"    {name}")
        return

    file_name = str(files[0])
    _run_file(file_name)


def _kill(path: str, args: list[str] | None = None, context: RunContext = None):
    pids = []

    # Если аргументы не заданы, то убиваем все процессы
    if not args:
        pids += kill_servers(path)
        pids += kill_explorers(path)
        pids += kill_designers(path)

    else:
        flags = []
        for arg in args:
            if arg.startswith("-"):
                arg = arg.strip("-").lower()
                flags += arg  # NOTE: "se" будут добавлены как "s" и "e"

        # -a - убиваем все сервера и проводники из всех папок
        if "a" in flags:
            pids += kill_servers()
            pids += kill_explorers()
            pids += kill_designers()
        else:
            if "s" in flags:
                pids += kill_servers(path)

            if "e" in flags:
                pids += kill_explorers(path)

            if "d" in flags:
                pids += kill_designers(path)

    if not pids:
        print("Не удалось найти процессы!")


def _processes(path: str, args: list[str] | None = None, context: RunContext = None):
    class ProcessEnum(enum.Enum):
        Server = enum.auto()
        Explorer = enum.auto()
        Designer = enum.auto()

    type_by_processes = {
        ProcessEnum.Server: [],
        ProcessEnum.Explorer: [],
        ProcessEnum.Designer: [],
    }

    # all - показываем все процессы
    if args and args[0].lower().startswith("a"):
        path = None

    for p in get_processes(path):
        if is_server(p):
            type_by_processes[ProcessEnum.Server].append(p)
        elif is_explorer(p):
            type_by_processes[ProcessEnum.Explorer].append(p)
        elif is_designer(p):
            type_by_processes[ProcessEnum.Designer].append(p)

    for process_type, processes in type_by_processes.items():
        if not processes:
            continue

        print(f"{process_type.name} ({len(processes)}):")
        for p in processes:
            started_time = datetime.fromtimestamp(p.create_time())
            print(f"    #{p.pid}, запущено: {started_time:%d/%m/%Y %H:%M:%S}")

    if not any(type_by_processes.values()):
        print("Не удалось найти процессы!")


def _get_last_release_version(path: str, args: list[str] | None = None, context: RunContext = None):
    command = context.command
    version = command.version

    # Значение в днях передается в аргументах
    last_days = 30
    if args and args[0].isdigit():
        last_days = int(args[0])

    url_svn_path = get_settings(command.name)["svn_dev_url"]

    try:
        result = get_last_release_version(
            version=version,
            last_days=last_days,
            url_svn_path=url_svn_path,
        )
    except Exception as e:
        result = str(e)

    print(f"Последняя версия релиза для {version}: {result}\n")


def _find_release_versions(path: str, args: list[str] | None = None, context: RunContext = None):
    if context.command.version == "trunk":
        raise GoException("Команду нужно вызывать в релизных версиях!")

    if not args:
        raise GoException("Текст для поиска не указан!")

    text = args[0]

    # Значение в днях передается в аргументах
    last_days = 30
    if len(args) > 1 and args[1].isdigit():
        last_days = int(args[1])

    command = context.command
    version = command.version

    url_svn_path = get_settings(command.name)["svn_dev_url"]

    try:
        result = find_release_version(
            text=text,
            version=version,
            last_days=last_days,
            url_svn_path=url_svn_path,
        )

    except Exception as e:
        result = str(e)

    print(f"Коммит с {text!r} в {version} попал в версию: {result}\n")


def _find_versions(path: str, args: list[str] | None = None, context: RunContext = None):
    command = context.command

    if not args:
        raise GoException("Текст для поиска не указан!")

    text = args[0]

    # Значение в днях передается в аргументах
    last_days = 30
    if len(args) > 1 and args[1].isdigit():
        last_days = int(args[1])

    url_svn_path = get_settings(command.name)["svn_dev_url"]

    try:
        versions = search_by_versions(
            text=text,
            last_days=last_days,
            url_svn_path=url_svn_path,
        )
        result = ", ".join(versions)

    except Exception as e:
        result = str(e)

    print(f"Строка {text!r} встречается в версиях: {result}")


def _manager_up(path: str, _: list[str] | None = None, context: RunContext = None):
    path = Path(path)

    # NOTE: "C:\DEV__RADIX\manager\manager\bin\manager.cmd" -> "C:\DEV__RADIX\manager"
    root_dir = path.parent.parent.parent
    path_from = root_dir / "radix_manager/distrib"
    files = list(path_from.rglob("*.zip"))
    if not files:
        print(f"Не найдены файлы в {path_from}")
        return

    path_to = root_dir / "optt_manager/upgrades"
    print(f"Перемещение файлов в {path_to}:")

    for file in files:
        print(f"    File: {file.name}")

        new_file = path_to / file.name

        # Если файл уже есть, то удаляем его - мало ли в каком он состоянии
        if new_file.exists():
            new_file.unlink()

        shutil.move(file, new_file)


def _manager_clean(path: str, _: list[str] | None = None, context: RunContext = None):
    path = Path(path)

    # NOTE: "C:\DEV__RADIX\manager\manager\bin\manager.cmd" -> "C:\DEV__RADIX\manager"
    root_dir = path.parent.parent.parent
    path_from = root_dir / "optt_manager/upgrades.backup"
    files = list(path_from.rglob("*.zip"))
    if not files:
        print(f"Не найдены файлы в {path_from}")
        return

    print(f"Удаление файлов из {path_from}:")
    for file in files:
        print(f"    Файл: {file.name}")
        file.unlink()


def _server(path: str, args: list[str] | None = None, _: RunContext = None):
    default_file: str = "!!server.cmd"
    arg_by_file: dict[str, str] = {
        "ora": default_file,
        "pg": "!!server-postgres.cmd",
    }
    file_name: str = default_file
    if args:
        for arg, value in arg_by_file.items():
            if arg in args:
                file_name = value
                break

    full_file_name: str = str(Path(path) / file_name)
    _run_file(full_file_name)


def _svn_update(path: str, args: list[str] | None = None, context: RunContext = None):
    force = False

    # force - обновляемся, даже если сборка сломана
    if args and "-f" in args:
        force = True

    command = context.command
    settings = get_settings(command.name)

    jenkins_url = settings.get("jenkins_url")
    if jenkins_url:
        try:
            do_check_jenkins_job(jenkins_url, command.version)
        except JenkinsJobCheckException as e:
            if not force:
                text = "Чтобы все-равно загрузить повторите с аргументом -f"
                print(f"{e}\n\n{text}")
                return

    command_svn = r'start /b "" TortoiseProc /command:update /path:"{path}"'
    command_svn = command_svn.format(path=path)

    print(f"Запуск: {context.description} в {path}")
    os.system(command_svn)


__SETTINGS = {
    "__radix_base": {
        "options": {
            "version": AvailabilityEnum.OPTIONAL,
            "what": AvailabilityEnum.REQUIRED,
            "args": AvailabilityEnum.OPTIONAL,
            "default_version": "trunk",
        },
        "whats": {
            "designer": "!!designer.cmd",
            "explorer": "!!explorer.cmd",
            "server": (
                "server",
                _server,
            ),
            "compile": "!build_ads__pause.bat",
            "build": "!build_kernel__pause.cmd",
            "update": (
                "svn update",
                _svn_update,
            ),
            "log": (
                "svn log",
                r'start /b "" TortoiseProc /command:log /path:"{path}" /findstring:"{find_string}"',
            ),
            "cleanup": (
                "svn cleanup",
                'start /b "" TortoiseProc /command:cleanup /path:"{path}" /cleanup /nodlg /closeonend:2',
            ),
            "revert": (
                "svn revert",
                'start /b "" TortoiseProc /command:revert /path:"{path}"',
            ),
            "modifications": (
                "svn show modifications dialog",
                'start /b "" TortoiseProc /command:repostatus /path:"{path}"',
            ),
            "run": _run_path,
            "kill": _kill,
            "processes": _processes,
            "get_last_release_version": _get_last_release_version,
            "find_release_versions": _find_release_versions,
            "find_versions": _find_versions,
        },
    },
    "tx": {
        "base": "__radix_base",
        "path": "C:/DEV__TX",
        "base_version": "3.2.",
        "jenkins_url": "{URL_JENKINS}/job/TX_{version}_build/lastBuild/api/json?tree=result,timestamp",
        "svn_dev_url": "svn+cplus://svn2.compassplus.ru/twrbs/trunk/dev",
    },
    "optt": {
        "base": "__radix_base",
        "path": "C:/DEV__OPTT",
        "base_version": "2.1.",
        "jenkins_url": "{URL_JENKINS}/job/OPTT_{version}_build/lastBuild/api/json?tree=result,timestamp",
        "svn_dev_url": "svn+cplus://svn2.compassplus.ru/twrbs/csm/optt/dev",
    },
    "__simple_base": {
        "options": {
            "version": AvailabilityEnum.PROHIBITED,
            "what": AvailabilityEnum.PROHIBITED,
            "args": AvailabilityEnum.PROHIBITED,
        }
    },
    "manager": {
        "base": "__simple_base",
        "path": "C:/DEV__RADIX/manager/manager/bin/manager.cmd",
        "options": {
            "what": AvailabilityEnum.OPTIONAL,
        },
        "whats": {
            "up": _manager_up,
            "clean": _manager_clean,
        },
    },
    "doc": {
        "base": "__simple_base",
        "path": "C:/Program Files (x86)/DocFetcher/DocFetcher.exe",
    },
    "specifications": {
        "base": "__simple_base",
        "path": "C:/DOC/Specifications",
    },
}
SETTINGS = settings_preprocess(__SETTINGS)

ABOUT_TEXT = r"""
RUN:
  go <name> <version> <what> - Run tool
  go <name> <what>           - Run tool (trunk version)
  go open <name> <version>   - Open dir version
  go open <name>             - Open dir
  go <name>                  - Print versions

SUPPORTED NAMES:
  {}

EXAMPLES:
  > go optt trunk designer
    Run: "C:/DEV__OPTT/trunk_optt/!!designer.cmd"

  > go tx 3.2.6.10 server
    Run: "C:/DEV__TX/3.2.6.10/!!server.cmd"

  > go tx 6 server
    Run: "C:/DEV__TX/3.2.6.10/!!server.cmd"

  > go tx 3.2.6,3.2.7,trunk server
    Run: "C:/DEV__TX/3.2.6.10/!!server.cmd"

  > go tx 3.2.6-trunk server
    Run: "C:/DEV__TX/3.2.6.10/!!server.cmd"

  > $ go tx 35 u
    Run: svn update in C:\DEV__TX\3.2.35.10

  > $ go tx 35 u -f
    Run: svn update in C:\DEV__TX\3.2.35.10

  > go tx designer
    Run: "C:/DEV__TX/trunk_tx/!!designer.cmd"

  > go tx get_last
    Run: tx call 'get_last_release_version'
    Последняя версия релиза для trunk: 3.2.36.10
    
  > go tx 34 get_last
    Run: tx call 'get_last_release_version'
    Последняя версия релиза для 3.2.34.10: 3.2.34.10.17

  > go tx find_ver TXI-8197
    Run: tx call 'find_versions' (['TXI-8197'])
    Строка 'TXI-8197' встречается в версиях: trunk, 3.2.36.10, 3.2.35.10, 3.2.34.10
    
  > go tx 34-35 find_rele TXI-8197
    Run: tx call 'find_release_versions' (['TXI-8197'])
    Коммит с 'TXI-8197' в 3.2.34.10 попал в версию: 3.2.34.10.18
    
    Run: tx call 'find_release_versions' (['TXI-8197'])
    Коммит с 'TXI-8197' в 3.2.35.10 попал в версию: 3.2.35.10.11

  > go open optt trunk
    Open: "C:/DEV__OPTT/trunk_optt"

  > go open optt
    Open: "C:/DEV__OPTT"

  > go optt
    Supported versions: 2.1.10, trunk_optt
    Supported <what>: build, cleanup, compile, designer, explorer, log, server, update
    
  > go optt kill
  > go optt kill -d
  > go optt kill -s
  > go optt kill -e
  > go optt kill -a
  > go optt kill -se
""".format(
    ", ".join(SETTINGS.keys()),
).strip()


def all_options_is_prohibited(name: str) -> bool:
    options = get_settings(name)["options"]
    return (
        options["version"] == AvailabilityEnum.PROHIBITED
        and options["what"] == AvailabilityEnum.PROHIBITED
        and options["args"] == AvailabilityEnum.PROHIBITED
    )


def resolve_name(alias: str) -> str:
    supported = list(SETTINGS)
    shadow_supported = {from_ghbdtn(x): x for x in supported}

    # Поиск среди списка
    name = get_similar_value(alias, supported)
    if not name:
        # Попробуем найти среди транслитерованных
        name = get_similar_value(alias, shadow_supported)
        if not name:
            raise UnknownNameException(alias, supported)

        # Если удалось найти
        name = shadow_supported[name]

    return name


def resolve_whats(name: str, alias: str | None) -> list[str]:
    items = []
    if not alias:
        return items

    supported = list(get_settings(name)["whats"])
    shadow_supported = {from_ghbdtn(x): x for x in supported}

    for alias_what in alias.split("+"):
        # Поиск среди списка
        what = get_similar_value(alias_what, supported)
        if not what:
            # Попробуем найти среди транслитерованных
            what = get_similar_value(alias_what, shadow_supported)
            if not what:
                raise UnknownWhatException(alias_what, supported)

            # Если удалось найти
            what = shadow_supported[what]

        items.append(what)

    return items


def resolve_version(name: str, alias: str, versions: list[str] | None = None) -> str:
    settings = get_settings(name)

    supported = versions
    if not supported:
        supported = settings["versions"]

    shadow_supported = {from_ghbdtn(x): x for x in supported}

    # Если короткая версия, нужно ее расширить, добавив основание версии
    if is_like_a_short_version(alias):
        base_version = settings.get("base_version")
        if not base_version:
            text = (
                f'Атрибут "base_settings", используемый с короткой версией (="{alias}"), '
                f'должен быть определен в SETTINGS для "{name}"'
            )
            raise GoException(text)

        # Составление полной версии
        alias = base_version + alias

    # Поиск среди списка
    version = get_similar_value(alias, supported)
    if not version:
        # Попробуем найти среди транслитерованных
        version = get_similar_value(alias, shadow_supported)
        if not version:
            raise UnknownNameException(alias, supported)

        # Если удалось найти
        version = shadow_supported[version]

    return version


def get_file_by_what(name: str, alias: str | None) -> str | tuple[str, str] | None:
    whats = resolve_whats(name, alias)
    if not whats:
        return
    what = whats[0]
    return get_settings(name)["whats"][what]


def get_similar_version_path(name: str, version: str) -> str:
    supported = get_settings(name)["versions"]
    version = resolve_version(name, version, supported)
    return supported[version]


def _run_file(file_name: str):
    dir_file_name = os.path.dirname(file_name)
    file_name = os.path.normpath(file_name)

    print(f"Запуск: {file_name!r}")

    # Move to active dir
    os.chdir(dir_file_name)

    # Run
    os.startfile(file_name)


def _open_dir(path: str):
    if os.path.isfile(path):
        dir_file_name = os.path.dirname(path)
    else:
        dir_file_name = path

    print(f"Открытие: {dir_file_name!r}")

    # Open
    os.startfile(dir_file_name)


def go_run(
    name: str,
    version: str | None = None,
    what: str | None = None,
    args: list[str] | None = None,
    context_command: Command = None,
):
    if args is None:
        args = []

    # Если по <name> указывается файл, то сразу его и запускаем
    path = get_path_by_name(name)
    value = get_file_by_what(name, what)

    # Если по <name> указывается файл, то сразу его и запускаем
    if (os.path.isfile(path) and not what and not args) or all_options_is_prohibited(name):
        _run_file(path)
        return

    if version:
        path = get_similar_version_path(name, version)

    # Если в <whats> функция, вызываем её
    if callable(value):
        print(f"Запуск: {name} вызов {what!r}" + (f" ({args})" if args else ""))
        value(path, args, RunContext(context_command))
        return

    dir_file_name = get_similar_version_path(name, version)

    # Move to active dir
    os.chdir(dir_file_name)

    if isinstance(value, str):
        file_name = dir_file_name + "/" + value
        _run_file(file_name)
        return

    description, command = value

    # Если функция - вызываем
    if callable(command):
        command(path, args, RunContext(context_command, description))
        return

    find_string = "" if not args else args[0]
    command = command.format(path=dir_file_name, find_string=find_string)

    print(f"Запуск: {description} в {dir_file_name}")
    os.system(command)


def parse_cmd_args(args: list[str]) -> list[Command]:
    args = args.copy()
    name, whats = [None] * 2
    versions = []

    # Первый аргумент <name>
    if args:
        name = args.pop(0).lower()
        name = resolve_name(name)

    options = get_settings(name)["options"]
    maybe_version = options["version"] != AvailabilityEnum.PROHIBITED
    maybe_what = options["what"] != AvailabilityEnum.PROHIBITED

    # Второй аргумент это или <version>, или <what>
    if (maybe_version or maybe_what) and args:
        alias = args.pop(0).lower()

        if (
            is_like_a_version(alias)
            and options["version"] != AvailabilityEnum.PROHIBITED
        ):
            # Например, "3.2.23,3.2.24,3.2.25,trunk"
            if "," in alias:
                for x in alias.split(","):
                    version = resolve_version(name, x)
                    versions.append(version)

            elif "-" in alias:  # Например, "3.2.23-trunk"
                start, end = alias.split("-")
                start = resolve_version(name, start)
                end = resolve_version(name, end)

                found = False
                for version in get_settings(name)["versions"]:
                    if start == version:
                        found = True

                    if not found:
                        continue

                    versions.append(version)

                    if end in version:
                        break

            else:
                version = resolve_version(name, alias)
                versions.append(version)

        elif options["what"] != AvailabilityEnum.PROHIBITED:
            whats = resolve_whats(name, alias)

    # Третий аргумент <what>
    if maybe_what and args and not whats:
        whats = args.pop(0).lower()
        whats = resolve_whats(name, whats)

    if not versions:
        versions = [None]

    if not whats:
        whats = [None]

    commands = []
    for version in versions:
        for what in whats:
            commands.append(
                Command(name, version, what, args)
            )
    return commands


def run(args: list[str]):
    try:
        if args[0] in ["open", from_ghbdtn("open")]:
            args.pop(0)

            if len(args) == 1:
                path = get_path_by_name(args[0])
                _open_dir(path)

            elif len(args) >= 2:
                name, version = args[:2]
                path = get_similar_version_path(name, version)
                _open_dir(path)

            else:
                _print_help()

            return

        for command in parse_cmd_args(args):
            command.run()

    except ParameterAvailabilityException as e:
        name = e.command.name
        settings = get_settings(name)

        # Если для сущности параметр версии возможен
        if settings["options"]["version"] != AvailabilityEnum.PROHIBITED:
            supported_versions = ", ".join(sorted(settings["versions"]))
            print(f"Поддерживаемые версии: {supported_versions}")

        # Если для сущности параметр what возможен
        if settings["options"]["what"] != AvailabilityEnum.PROHIBITED:
            supported_whats = ", ".join(sorted(settings["whats"]))
            print(f"Поддерживаемые <what>: {supported_whats}")

    except GoException as e:
        # Если передан флаг отладки
        if args[-1].lower().startswith("-d"):
            print(traceback.format_exc())
        else:
            print(e)


def _print_help():
    print(ABOUT_TEXT)
    sys.exit()


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        _print_help()

    run(args)
