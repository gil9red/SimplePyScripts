#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import codecs
import json
import logging
import sys
import time

from logging.handlers import RotatingFileHandler
from typing import Callable, List, Union
from pathlib import Path

import requests

from all_config import API_ID, TO

# Import https://github.com/gil9red/SimplePyScripts/blob/8fa9b9c23d10b5ee7ff0161da997b463f7a861bf/wait/wait.py
# Absolute path. Analog '../wait'
sys.path.append(str(Path(__file__).resolve().parent.parent / 'wait'))

from wait import wait


def make_backslashreplace_console():
    # При выводе юникодных символов в консоль винды
    # Возможно, не только для винды, но и для любой платформы стоит использовать
    # эту настройку -- мало какие проблемы могут встретиться
    if sys.platform == 'win32':
        try:
            sys.stdout = codecs.getwriter(sys.stdout.encoding)(sys.stdout.detach(), 'backslashreplace')
            sys.stderr = codecs.getwriter(sys.stderr.encoding)(sys.stderr.detach(), 'backslashreplace')

        except AttributeError:
            # ignore "AttributeError: '_io.BufferedWriter' object has no attribute 'encoding'"
            pass


def get_logger(name, file='log.txt', encoding='utf-8', log_stdout=True, log_file=True) -> 'logging.Logger':
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s')

    if log_file:
        fh = RotatingFileHandler(file, maxBytes=10000000, backupCount=5, encoding=encoding)
        fh.setFormatter(formatter)
        log.addHandler(fh)

    if log_stdout:
        sh = logging.StreamHandler(stream=sys.stdout)
        sh.setFormatter(formatter)
        log.addHandler(sh)

    return log


def send_sms(api_id: str, to: str, text: str, log):
    api_id = api_id.strip()
    to = to.strip()

    if not api_id or not to:
        log.warning('Параметры api_id или to не указаны, отправка СМС невозможна!')
        return

    log.info(f'Отправка sms: {text!r}')

    if len(text) > 70:
        text = text[:70-3] + '...'
        log.info(f'Текст sms будет сокращено, т.к. слишком длинное (больше 70 символов): {text!r}')

    # Отправляю смс на номер
    url = 'https://sms.ru/sms/send?api_id={api_id}&to={to}&text={text}'.format(
        api_id=api_id,
        to=to,
        text=text
    )
    log.debug(repr(url))

    while True:
        try:
            rs = requests.get(url)
            log.debug(repr(rs.text))
            break

        except:
            log.exception("При отправке sms произошла ошибка:")
            log.debug('Через 5 минут попробую снова...')

            # Wait 5 minutes before next attempt
            time.sleep(5 * 60)


def simple_send_sms(text: str, log=None):
    # Если логгер не определен, тогда создаем свой, который логирует в консоль
    if not log:
        log = get_logger('all_common', log_file=False)

    return send_sms(API_ID, TO, text, log)


def run_notification_job(
    log__or__log_name: Union['logging.Logger', str],
    file_name_items: str,
    get_new_items: Callable[[], List[str]],
    notified_by_sms=True,
    timeout={'weeks': 1},
    timeout_exception_seconds=5 * 60,
    format_first_start_detected='Обнаружен первый запуск',
    format_current_items='Текущий список (%s): %s',
    format_get_items='Запрос списка',
    format_items='Список (%s): %s',
    format_new_item='Появился новый элемент "%s"',
    format_no_new_items='Новых элементов нет',
    format_on_exception='Ошибка:',
    format_on_exception_next_attempt='Через 5 минут попробую снова...',
):
    log = log__or__log_name
    if isinstance(log, str):
        log = get_logger(log)

    def save_items(items: List[str]):
        with open(file_name_items, mode='w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=4)

    def read_items() -> List[str]:
        try:
            with open(file_name_items, encoding='utf-8') as f:
                obj = json.load(f)

                # Должен быть список, но если в файле будет что-то другое -- это будет неправильно
                if not isinstance(obj, list):
                    return []

                return obj

        except:
            return []

    FILE_NAME_SKIP = Path('skip')

    # Загрузка текущего списка из файла
    current_items = read_items()
    log.debug(format_current_items, len(current_items), current_items)

    while True:
        if FILE_NAME_SKIP.exists():
            log.info('Обнаружен файл "%s", пропускаю проверку.', FILE_NAME_SKIP.name)
            wait(**timeout)
            continue

        try:
            log.debug(format_get_items)

            items = get_new_items()
            log.debug(format_items, len(items), items)

            # Если текущих список пустой
            if not current_items:
                log.debug(format_first_start_detected)

                current_items = items
                save_items(current_items)

            else:
                new_items = set(items) - set(current_items)
                if new_items:
                    current_items = items
                    save_items(current_items)

                    for item in new_items:
                        text = format_new_item % item
                        log.debug(text)

                        if notified_by_sms:
                            simple_send_sms(text, log)

                else:
                    log.debug(format_no_new_items)

            wait(**timeout)

        except:
            log.exception(format_on_exception)
            log.debug(format_on_exception_next_attempt)

            # Wait <timeout_exception_seconds> before next attempt
            time.sleep(timeout_exception_seconds)
