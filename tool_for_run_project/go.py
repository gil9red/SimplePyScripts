#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import copy
import os
import sys
import re

from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import Optional, List, Tuple, Union, Iterable, Dict

sys.path.append('..')
from from_ghbdtn import from_ghbdtn


class AvailabilityEnum(Enum):
    OPTIONAL = auto()
    REQUIRED = auto()
    PROHIBITED = auto()


class GoException(Exception):
    pass


class UnknownNameException(GoException):
    def __init__(self, name: str, supported: Iterable[str]):
        self.name = name
        self.supported = list(supported)

        super().__init__(f'Unknown name {self.name!r}, supported: {self.supported}')


class UnknownWhatException(GoException):
    def __init__(self, what: str, supported: Iterable[str]):
        self.what = what
        self.supported = list(supported)

        super().__init__(f'Unknown what {self.what!r}, supported: {self.supported}')


class UnknownVersionException(GoException):
    def __init__(self, version: str, supported: Iterable[str]):
        self.version = version
        self.supported = list(supported)

        super().__init__(f'Unknown version {self.version!r}, supported: {self.supported}')


class ParameterMissing(GoException):
    def __init__(self, name: str, param: str):
        self.name = name
        self.param = param

        super().__init__(f'For {self.name!r} the value <{self.param}> must not be set!')


class ParameterAvailabilityException(GoException):
    def __init__(self, command: 'Command', param: str, availability: AvailabilityEnum):
        if availability == AvailabilityEnum.REQUIRED:
            post_fix = 'must be set!'
        elif availability == AvailabilityEnum.PROHIBITED:
            post_fix = 'must not be set!'
        else:
            raise GoException(f'Not supported availability: {availability}!')

        self.command = command
        self.param = param
        self.availability = availability

        super().__init__(f'For {self.command.name!r} the value <{self.param}> ' + post_fix)


@dataclass
class Command:
    name: str
    version: Optional[str] = None
    what: Optional[str] = None
    args: Optional[List[str]] = None

    def _check_parameter(self, param: str):
        settings = SETTINGS[self.name]

        value = getattr(self, param)
        settings_param = settings['options'][param]
        if settings_param == AvailabilityEnum.REQUIRED:
            if not value:
                raise ParameterAvailabilityException(self, param, settings_param)

        elif settings_param == AvailabilityEnum.PROHIBITED:
            if value:
                raise ParameterAvailabilityException(self, param, settings_param)

    def run(self):
        settings = SETTINGS[self.name]

        settings_version = settings['options']['version']
        if settings_version == AvailabilityEnum.OPTIONAL and not self.version:
            self.version = resolve_version(self.name, settings['options']['default_version'])

        self._check_parameter('version')
        self._check_parameter('what')
        self._check_parameter('args')

        go_run(self.name, self.version, self.what, self.args)


# SOURCE: https://stackoverflow.com/a/20666342/5909792
def merge_dicts(source: Dict, destination: Dict) -> Dict:
    for key, value in source.items():
        if isinstance(value, dict):
            # Get node or create one
            node = destination.setdefault(key, dict())
            merge_dicts(value, node)
        else:
            destination[key] = value

    return destination


def is_like_a_short_version(value: str) -> bool:
    # Вариант .isdigit() для коротких версий, не 3.2.25, а 25
    return value.isdigit()


def is_like_a_version(value: str) -> bool:
    return (
        'trunk' in value
        or bool(re.search(r'\d+(\.\d+)+', value))
        or is_like_a_short_version(value)
        or '-' in value  # Example: "23-25" or "23-trunk"
        or ',' in value  # Example: "23,24,25" or "23,24,25,trunk"
    )


def get_settings(name: str) -> dict:
    name = resolve_name(name)
    return SETTINGS[name]


def get_path_by_name(name: str) -> str:
    settings = get_settings(name)
    return settings['path']


def get_versions_by_path(path: str) -> Dict[str, str]:
    version_by_path = dict()

    dir_path = Path(path)

    if dir_path.is_dir():
        for path in dir_path.iterdir():
            if path.is_dir() and is_like_a_version(path.name):
                version_by_path[path.name] = str(path)

    return version_by_path


def _print_pretty_SETTINGS():
    import json
    print(json.dumps(SETTINGS, indent=4, default=str))
    sys.exit()


def settings_preprocess(settings: Dict[str, Dict]) -> Dict[str, Dict]:
    new_settings = dict()

    # Update from bases
    for name, values in settings.items():
        if 'base' in values:
            # Removing base name
            base_name = values.pop('base')
            base_values = settings[base_name]
            new_settings[name] = copy.deepcopy(base_values)

        if name not in new_settings:
            new_settings[name] = dict()

        merge_dicts(values, new_settings[name])

        if 'path' in new_settings[name] and new_settings[name]['options']['version'] != AvailabilityEnum.PROHIBITED:
            path = new_settings[name]['path']
            new_settings[name]['versions'] = get_versions_by_path(path)

    # Removing private names
    private_names = [name for name in new_settings if name.startswith('__')]
    for name in private_names:
        new_settings.pop(name)

    return new_settings


SETTINGS = {
    '__radix_base': {
        'options': {
            'version': AvailabilityEnum.OPTIONAL,
            'what': AvailabilityEnum.REQUIRED,
            'args': AvailabilityEnum.OPTIONAL,
            'default_version': 'trunk',
        },
        'whats': {
            'designer': '!!designer.cmd',
            'explorer': '!!explorer.cmd',
            'server':   '!!server.cmd',
            'compile':  '!build_ads__pause.bat',
            'build':    '!build_kernel__pause.cmd',
            'update':   ('svn update', r'start /b "" TortoiseProc /command:update /path:"{path}"'),
            'log':      ('svn log', r'start /b "" TortoiseProc /command:log /path:"{path}" /findstring:"{find_string}"'),
            'cleanup':  ('svn cleanup', 'start /b "" TortoiseProc /command:cleanup /path:"{path}" /cleanup /nodlg /closeonend:2'),
        },
    },
    'tx': {
        'base': '__radix_base',
        'path': 'C:/DEV__TX',
        'base_version': '3.2.',
    },
    'optt': {
        'base': '__radix_base',
        'path': 'C:/DEV__OPTT',
        'base_version': '2.1.',
    },
    '__simple_base': {
        'options': {
            'version': AvailabilityEnum.PROHIBITED,
            'what': AvailabilityEnum.PROHIBITED,
            'args': AvailabilityEnum.PROHIBITED,
        }
    },
    'manager': {
        'base': '__simple_base',
        'path': 'C:/manager_1_2_11_23_8/manager/bin/manager.cmd',
    },
    'doc': {
        'base': '__simple_base',
        'path': 'C:/Program Files (x86)/DocFetcher/DocFetcher.exe',
    },
    'specifications': {
        'base': '__simple_base',
        'path': 'C:/DOC/Specifications',
    },
}

SETTINGS = settings_preprocess(SETTINGS)
# _print_pretty_SETTINGS()

ABOUT_TEXT = '''\
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

  > go tx designer
    Run: "C:/DEV__TX/trunk_tx/!!designer.cmd"

  > go open optt trunk
    Open: "C:/DEV__OPTT/trunk_optt"

  > go open optt
    Open: "C:/DEV__OPTT"

  > go optt
    Supported versions: 2.1.10, trunk_optt
    Supported <what>: build, cleanup, compile, designer, explorer, log, server, update
'''.format(
    ', '.join(SETTINGS.keys()),
)


def get_similar_value(alias: str, items: Iterable) -> Optional[str]:
    if alias in items:
        return alias

    # Ищем похожие ключи по начальной строке
    keys = [key for key in items if key.startswith(alias)]

    # Нашли одну вариацию - подходит
    if len(keys) == 1:
        return keys[0]


def has_similar_value(alias: str, items: list) -> bool:
    return get_similar_value(alias, items) is not None


def all_options_is_prohibited(name: str) -> bool:
    options = get_settings(name)['options']
    return (
        options['version'] == AvailabilityEnum.PROHIBITED
        and options['what'] == AvailabilityEnum.PROHIBITED
        and options['args'] == AvailabilityEnum.PROHIBITED
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


def resolve_whats(name: str, alias: str) -> List[str]:
    supported = list(get_settings(name)['whats'])
    shadow_supported = {from_ghbdtn(x): x for x in supported}

    items = []
    for alias_what in alias.split('+'):
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


def resolve_version(name: str, alias: str, versions: List[str] = None) -> str:
    settings = get_settings(name)

    supported = versions
    if not supported:
        supported = settings['versions']

    # Если короткая версия, нужно ее расширить, добавив основание версии
    if is_like_a_short_version(alias):
        base_version = settings.get('base_version')
        if not base_version:
            text = f'Attribute "base_settings", using with short versions (="{alias}"), ' \
                   f'must be defined in SETTINGS for "{name}"'
            raise GoException(text)

        # Составление полной версии
        alias = base_version + alias

    # Поиск среди списка
    version = get_similar_value(alias, supported)
    if not version:
        raise UnknownVersionException(alias, supported)

    return version


def get_file_by_what(name: str, alias: str) -> Union[str, Tuple[str, str]]:
    what = resolve_whats(name, alias)[0]
    return get_settings(name)['whats'][what]


def get_similar_version_path(name: str, version: str) -> str:
    supported = get_settings(name)['versions']
    version = resolve_version(name, version, supported)
    return supported[version]


def _run_file(file_name: str):
    dir_file_name = os.path.dirname(file_name)
    file_name = os.path.normpath(file_name)

    print(f'Run: {file_name!r}')

    # Move to active dir
    os.chdir(dir_file_name)

    # Run
    os.startfile(file_name)


def _open_dir(path: str):
    if os.path.isfile(path):
        dir_file_name = os.path.dirname(path)
    else:
        dir_file_name = path

    print(f'Open: {dir_file_name!r}')

    # Open
    os.startfile(dir_file_name)


def go_run(name: str, version: Optional[str] = None, what: Optional[str] = None, args: List[str] = None):
    if args is None:
        args = []

    # Если по <name> указывается файл, то сразу его и запускаем
    path = get_path_by_name(name)
    if os.path.isfile(path) or all_options_is_prohibited(name):
        _run_file(path)
        return

    dir_file_name = get_similar_version_path(name, version)

    # Move to active dir
    os.chdir(dir_file_name)

    value = get_file_by_what(name, what)
    if isinstance(value, str):
        file_name = dir_file_name + '/' + value
        _run_file(file_name)
    else:
        description, command = value

        find_string = '' if not args else args[0]
        command = command.format(path=dir_file_name, find_string=find_string)

        print(f'Run: {description} in {dir_file_name}')
        os.system(command)


def parse_cmd_args(arguments: List[str]) -> List[Command]:
    arguments = arguments.copy()
    name, whats, args = [None] * 3
    versions = []

    # Первый аргумент <name>
    if arguments:
        name = arguments.pop(0).lower()
        name = resolve_name(name)

    options = get_settings(name)['options']
    maybe_version = options['version'] != AvailabilityEnum.PROHIBITED
    maybe_what = options['what'] != AvailabilityEnum.PROHIBITED

    # Второй аргумент это или <version>, или <what>
    if (maybe_version or maybe_what) and arguments:
        alias = arguments.pop(0).lower()

        if is_like_a_version(alias) and options['version'] != AvailabilityEnum.PROHIBITED:
            # Например, "3.2.23,3.2.24,3.2.25,trunk"
            if ',' in alias:
                for x in alias.split(','):
                    version = resolve_version(name, x)
                    versions.append(version)

            elif '-' in alias:  # Например, "3.2.23-trunk"
                start, end = alias.split('-')
                start = resolve_version(name, start)
                end = resolve_version(name, end)

                found = False
                for version in get_settings(name)['versions']:
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

        elif options['what'] != AvailabilityEnum.PROHIBITED:
            whats = resolve_whats(name, alias)

    # Третий аргумент <what>
    if maybe_what and arguments and not whats:
        whats = arguments.pop(0).lower()
        whats = resolve_whats(name, whats)

    if not versions:
        versions = [None]

    if not whats:
        whats = [None]

    args = arguments

    commands = []
    for version in versions:
        for what in whats:
            commands.append(Command(name, version, what, args))
    return commands


def run(arguments: List[str]):
    if arguments[0] in ['open', from_ghbdtn('open')]:
        arguments.pop(0)

        if len(arguments) == 1:
            path = get_path_by_name(arguments[0])
            _open_dir(path)

        elif len(arguments) >= 2:
            name, version = arguments[:2]
            path = get_similar_version_path(name, version)
            _open_dir(path)

        else:
            _print_help()

        return

    for command in parse_cmd_args(arguments):
        try:
            command.run()
        except ParameterAvailabilityException as e:
            name = e.command.name
            settings = get_settings(name)

            # Если для сущности параметр версии возможен
            if settings['options']['version'] != AvailabilityEnum.PROHIBITED:
                supported_versions = ", ".join(sorted(settings['versions']))
                print(f'Supported versions: {supported_versions}')

            # Если для сущности параметр what возможен
            if settings['options']['what'] != AvailabilityEnum.PROHIBITED:
                supported_whats = ", ".join(sorted(settings['whats']))
                print(f'Supported <what>: {supported_whats}')


def _print_help():
    print(ABOUT_TEXT)
    sys.exit()


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        _print_help()

    run(args)
