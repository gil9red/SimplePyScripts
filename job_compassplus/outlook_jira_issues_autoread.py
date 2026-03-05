#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import argparse
import email
import imaplib
import re
import time

from dataclasses import dataclass
from datetime import datetime, timedelta
from email.header import decode_header
from email.utils import parseaddr
from typing import Any

from root_config import JIRA_HOST
from root_common import session


PATTERN_JIRA: re.Pattern = re.compile(r"\((\w+-\d+)\)")


@dataclass
class IssueInfo:
    key: str
    is_done: bool
    updated: datetime | None
    resolution_date: datetime | None


def get_issue_info(issue_key: str) -> IssueInfo:
    def _get_datetime(value: str) -> datetime | None:
        if value:
            return datetime.fromisoformat(value).replace(tzinfo=None)

    url_issue: str = f"{JIRA_HOST}/rest/api/latest/issue/{issue_key}"

    rs = session.get(url_issue)
    rs.raise_for_status()

    rs_fields: dict[str, Any] = rs.json()["fields"]

    return IssueInfo(
        key=issue_key,
        is_done=rs_fields["status"]["statusCategory"]["key"] == "done",
        updated=_get_datetime(rs_fields.get("updated")),
        resolution_date=_get_datetime(rs_fields.get("resolutiondate")),
    )


def get_args():
    parser = argparse.ArgumentParser(
        description="Скрипт для автоматического прочтения неактуальных писем из Jira в Outlook."
    )

    # Обязательные параметры
    parser.add_argument(
        "-u",
        "--user",
        required=True,
        help="Логин (email) от почты",
    )
    parser.add_argument(
        "-p",
        "--password",
        required=True,
        help="Пароль от почты (или пароль приложения)",
    )
    parser.add_argument(
        "-f",
        "--folder",
        default="INBOX",
        help="Папка для поиска (например, INBOX или 'Jira/Issues', по умолчанию: %(default)s))",
    )

    # Опциональные параметры
    parser.add_argument(
        "--server",
        default="mail.compassplus.com",
        help="Адрес IMAP сервера (по умолчанию: %(default)s)",
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Ограничение количества обрабатываемых писем (для тестирования, например 100)",
    )

    # Флаг прочтения (action='store_true' делает его булевым: если указан - True, если нет - False)
    parser.add_argument(
        "--mark",
        action="store_true",
        help="Если указан, письма при совпадении условий будут отмечены как прочитанные на сервере",
    )

    return parser.parse_args()


def process(
    user: str,
    password: str,
    server: str,
    folder: str,
    limit: int | None = None,
    mark_as_read: bool = False,
) -> None:
    print(f"Подключение к {server} для пользователя {user}...")

    mail = imaplib.IMAP4_SSL(server)
    mail.login(user, password)

    mail.select(f'"{folder}"')

    # Письма от старых к новым
    status, response = mail.search(None, "(UNSEEN)")

    issue_by_info: dict[str, Any] = dict()

    msg_ids = response[0].split()
    if limit:
        print(f"Лимит обработки: {limit} писем")
        msg_ids = msg_ids[:limit]

    for num in msg_ids:
        # BODY.PEEK[] - читаем, не меняя статус на "Прочитано"
        status, data = mail.fetch(num, "(BODY.PEEK[HEADER])")
        raw_email: bytes = data[0][1]
        msg = email.message_from_bytes(raw_email)

        # Декодируем заголовок
        decoded_parts = decode_header(msg["Subject"])

        subject = ""
        for content, encoding in decoded_parts:
            if isinstance(content, bytes):
                # Используем кодировку из письма, если её нет — пробуем utf-8
                enc = encoding if encoding else "utf-8"
                try:
                    subject += content.decode(enc)
                except (UnicodeDecodeError, LookupError):
                    # Если всё равно ошибка, декодируем с заменой битых символов
                    subject += content.decode("utf-8", errors="replace")
            else:
                # Если это уже строка (например, ASCII)
                subject += content

        raw_from: str = msg.get("From")
        name, email_address = parseaddr(raw_from)

        raw_date: str = msg.get("Date")
        date_tuple = email.utils.parsedate_tz(raw_date)
        local_date: datetime | None = None
        if date_tuple:
            local_date = datetime.fromtimestamp(
                email.utils.mktime_tz(date_tuple)
            ).replace(tzinfo=None)
        else:
            print(f"[#] Неправильная дата письма: {raw_date!r}")

        read_it: bool = False

        # NOTE: Можно оптимизировать и не ходить в API Jira, если письмо старше такой-то даты
        #       Но хочется посмотреть информацию по задачам из писем
        m: re.Match | None = PATTERN_JIRA.search(subject)
        if m:
            issue_key: str = m.group(1)
            print(
                "[+]",
                num,
                f"{local_date.strftime('%d.%m.%Y %H:%M:%S') if local_date else None}",
                repr(subject),
                repr(name),
                email_address,
                issue_key,
            )

            issue: IssueInfo | None = issue_by_info.get(issue_key)
            if not issue:
                try:
                    issue = get_issue_info(issue_key)
                    issue_by_info[issue_key] = issue
                except Exception as e:
                    print(f"[#] Не удалось получить информацию по задаче {issue_key!r}: {e}")

                time.sleep(1)

            print(f"    Информация по задаче: {issue if issue else '<неизвестно>'}")

            if issue:
                # Определяем запас времени (например, 10 минут)
                buffer = timedelta(minutes=10)

                # Если письма приходили до даты решения задачи, то уже не актуальные
                if (
                    issue.is_done
                    and issue.resolution_date
                    and local_date
                    # Если дата решения задачи больше даты отправки письма
                    and (issue.resolution_date - buffer) > local_date
                ):
                    print("    Письмо приходило раньше решения задачи")
                    read_it = True

        else:
            print(
                "[?]",
                num,
                f"{local_date.strftime('%d.%m.%Y %H:%M:%S') if local_date else None}",
                repr(subject),
                repr(name),
                email_address,
            )

        # Если прошло больше 1 месяца
        if local_date and (datetime.now() - timedelta(weeks=4)) > local_date:
            print("    Прошло больше 1 месяца")
            read_it = True

        if read_it:
            status_msg = (
                "[ПРОЧИТАНО]"
                if mark_as_read
                else "[DRY-RUN: БЫЛО БЫ ПРОЧИТАНО С ФЛАГОМ --mark]"
            )
            print(f"    {status_msg}")

            if mark_as_read:
                mail.store(num, "+FLAGS", r"\Seen")

    mail.logout()


if __name__ == "__main__":
    args = get_args()

    process(
        user=args.user,
        password=args.password,
        server=args.server,
        folder=args.folder,
        limit=args.limit,
        mark_as_read=args.mark,
    )
