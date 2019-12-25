#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from abc import ABCMeta, abstractmethod
from typing import List, Union
import os.path

from bs4 import BeautifulSoup
import requests

from common import (
    DIR_ERRORS, DIR_LOGS, NEED_LOGS, LOG_FORMAT, USER_AGENT,
    pretty_path, get_uniques, get_current_datetime_str, smart_comparing_names
)
from utils import dump


class Singleton(ABCMeta):
    _instances = dict()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)

        return cls._instances[cls]


class BaseParser(metaclass=Singleton):
    def __init__(self, need_logs=NEED_LOGS, dir_errors=DIR_ERRORS, dir_logs=DIR_LOGS, log_format=LOG_FORMAT):
        self.session = requests.session()
        self.session.headers['User-Agent'] = USER_AGENT

        self._dir_errors = pretty_path(dir_errors)
        self._dir_logs = pretty_path(dir_logs)

        self.game_name = ''
        self._need_logs = need_logs

        self._log = self._get_logger(log_format)

    @classmethod
    def instance(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def send_get(self, url: str, return_html=False, **kwargs) -> Union[requests.Response, BeautifulSoup]:
        rs = self.session.get(url, **kwargs)
        self._on_check_response(rs)

        if return_html:
            return BeautifulSoup(rs.content, 'html.parser')

        return rs

    def send_post(self, url: str, data=None, json=None, return_html=False, **kwargs) -> Union[requests.Response, BeautifulSoup]:
        rs = self.session.post(url, data=data, json=json, **kwargs)
        self._on_check_response(rs)

        if return_html:
            return BeautifulSoup(rs.content, 'html.parser')

        return rs

    def _save_error_response(self, rs: requests.Response):
        os.makedirs(self._dir_errors, exist_ok=True)

        file_name = pretty_path(
            f'{self._dir_errors}/{self.get_site_name()}_{self.game_name}_{get_current_datetime_str()}.dump'
        )
        self.log_debug(f'Save dump to {file_name}')

        data = dump.dump_all(rs, request_prefix=b'> ', response_prefix=b'< ')
        with open(file_name, 'wb') as f:
            f.write(data)

    def _on_check_response(self, rs: requests.Response):
        if rs.ok:
            return

        self.log_warn(f'Something went wrong...: status_code: {rs.status_code}\n{rs.text}')
        self._save_error_response(rs)

    def log_debug(self, msg, *args, **kwargs):
        self._need_logs and self._log.debug(msg, *args, **kwargs)

    def log_info(self, msg, *args, **kwargs):
        self._need_logs and self._log.info(msg, *args, **kwargs)

    def log_warn(self, msg, *args, **kwargs):
        self._need_logs and self._log.warning(msg, *args, **kwargs)

    def log_error(self, msg, *args, **kwargs):
        self._need_logs and self._log.error(msg, *args, **kwargs)

    def log_exception(self, msg, *args, **kwargs):
        self._need_logs and self._log.exception(msg, *args, **kwargs)

    @abstractmethod
    def get_site_name(self) -> str:
        pass

    @abstractmethod
    def _parse(self) -> List[str]:
        pass

    def is_found_game(self, game_name: str) -> bool:
        return smart_comparing_names(self.game_name, game_name)

    def get_game_genres(self, game_name: str) -> List[str]:
        self.game_name = game_name
        self.log_info(f'Search {game_name!r}...')

        try:
            genres = self._parse()
            genres = get_uniques(genres)

        except BaseException as e:
            self.log_exception('Parsing error:')
            raise e

        self.log_info(f'Genres: {genres}')
        return genres

    # SOURCE: https://github.com/gil9red/SimplePyScripts/blob/163c91d6882b548c904ad40703dac00c0a64e5a2/logger_example.py#L7
    def _get_logger(self, log_format: str, encoding='utf-8'):
        os.makedirs(self._dir_logs, exist_ok=True)

        site = self.get_site_name()

        name = 'parser_' + site
        file = self._dir_logs + '/' + site + '.txt'

        import logging
        log = logging.getLogger(name)
        log.setLevel(logging.DEBUG)

        formatter = logging.Formatter(log_format)

        from logging.handlers import RotatingFileHandler
        fh = RotatingFileHandler(file, maxBytes=10_000_000, backupCount=5, encoding=encoding)
        fh.setFormatter(formatter)
        log.addHandler(fh)

        import sys
        sh = logging.StreamHandler(stream=sys.stdout)
        sh.setFormatter(formatter)
        log.addHandler(sh)

        return log
