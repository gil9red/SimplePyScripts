#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import enum

from collections import Counter
from pathlib import Path
from typing import Final, Any, Generator, Sized

# TODO:
# from visa_base2_tc_counter import tc_by_counter


# TODO: Копия из https://github.com/gil9red/SimplePyScripts/blob/2cf402b71b89a0fe5ad1081f779060e8759c3836/split_list_into_evenly_sized_chunks.py
def chunks(l: Sized, n: int) -> Generator[Any, None, None]:
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i : i + n]


# TODO: из аргументов
DIR: Path = Path(r"C:\Users\ipetrash\Desktop\IMPORT_EXPORT\Visa Base 2")

# NOTE: Байты F0 - F9
# TODO: Мб в b"..."? вместо списка
EBCDIC_DIGITS: Final[list[int]] = [0xF0, 0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7, 0xF8, 0xF9]
ASCII_DIGITS: Final[list[int]] = [0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39]

IGNORED_TC: Final[list[str]] = ["90", "91", "92", "00"]

class FileType(enum.Enum):
    CTF = enum.auto()
    ITF = enum.auto()
    REPORT = enum.auto()

for f in DIR.rglob("*"):
    if not f.is_file():
        continue

    print(f"File: {f}")

    data: bytes = f.read_bytes()

    file_type: FileType
    lines: list[str]
    text: str

    if data[0] in EBCDIC_DIGITS and data[1] in EBCDIC_DIGITS:
        try:
            text = data.decode("cp500")
        except UnicodeDecodeError:
            print(f"[#] Not EBCDIC: {f}")
            continue

        # TODO: Проверить предположение
        # NOTE: Предположение, что в ITF хеш EBCDIC будет не F0 - F9
        # NOTE: Предположение, что в EBCDIC всегда будет ITF
        if data[2] in EBCDIC_DIGITS and data[3] in EBCDIC_DIGITS:
            file_type = FileType.CTF
        else:
            file_type = FileType.ITF

        # TODO: Проверить предположение
        # NOTE: Предположение, что в EBCDIC не будет перевода строк, нужно делить по 168 или 170 байтов
        # print(text)
        lines = list(chunks(text, n=168 if file_type == FileType.CTF else 170))

    elif data[0] in ASCII_DIGITS and data[1] in ASCII_DIGITS:
        try:
            text = data.decode("ascii")
        except UnicodeDecodeError:
            print(f"[#] Not ASCII: {f}")
            continue

        lines = text.splitlines()
        if len(lines[0]) == 168:
            file_type = FileType.CTF
        else:
            file_type = FileType.ITF

    elif data[1:8] == b"REPORT ":  # NOTE: Считаем, что у отчета кодировка будет ASCII
        # TODO: какое название дать? Report?
        #       file:///C:/DOC/Visa/documents-2026/BASE%20II%20Clearing%20Edit%20Package%20Reports%20Reference%20Guide%20Release%204,%20April%2023,%202026.pdf

        # TODO: Поддержка отчета C:\Users\ipetrash\Desktop\IMPORT_EXPORT\Visa Base 2\IMPORT_TEST\REPORT EP-100A\backup\EP100A.TXT
        # TODO: Поиск вида отчета по названиям EP-xxxx и VX-xxxx
        #       Примеры: EP–100A, EP–100B, ..., EP–199, EP–999
        #       Удаление пробелов добавить
        # TODO: Есть 2 вида отчета - обычный и расширенный, и мы как-то определяем какой сейчас. Для инфы нужно и это учитывать
        print("REPORT:", data)
        file_type = FileType.REPORT

        try:
            text = data.decode("ascii")
        except UnicodeDecodeError:
            print(f"[#] Not ASCII: {f}")
            continue

        # TODO: Тут вроде бы длина строк 133
        lines = text.splitlines()

    else:
        # TODO: Мб вообще удалить C:\Users\ipetrash\Desktop\IMPORT_EXPORT\Visa Base 2\TC33_Capture_Transaction\TWICH-11216\Testing PF3_VS_21144.csv

        print(f"[#] Not Visa Base II format: {f}")
        # raise Exception(f"[#] Not Visa Base II format: {f}")  # TODO:
        continue

    # TODO: Проверка на валидность - если первый 2 символа не 0 - 9, то это не CTF/ITF

    print("file_type:", file_type)
    print(f"Lines: {len(lines)}")
    # print(f"Lines ({len(lines)}):")
    # TODO:
    # print(*lines, sep="\n")

    # TODO: Анализ lines, чтобы найти TC, TCR
    if file_type == FileType.REPORT:
        # TODO:
        # 1/0
        import sys
        print("[#] TODO: REPORT not supported", file=sys.stderr)
    else:
        tc_by_counter = Counter()
        tc_tcr_by_counter = Counter()

        for line in lines:
            tc: str = line[:2]
            tcr: str = line[3:4] if file_type == FileType.CTF else line[5:6]

            if tc in IGNORED_TC:
                continue

            # TODO: для tc == 33 особенная логика разбора - есть те, что P17 имеют особенный идентификатор
            # TODO: для tc == 33 A особенная логика разбора - чтобы идентифицировать конкретные CPdd + TCR

            tc_by_counter.update([tc])
            tc_tcr_by_counter.update([f"{tc}-{tcr}"])

        # TODO: Отдельно, нужно группировать TC33 - там всякие дополнительные записи есть

        print("    TC:     " + ", ".join(f"{k}: {v}" for k, v in tc_by_counter.items()))
        print("    TC-TCR: " + ", ".join(f"{k}: {v}" for k, v in tc_tcr_by_counter.items()))

    print()


# for f in Path(r"C:\Users\ipetrash\Desktop\IMPORT_EXPORT\Visa Base 2").rglob("*"):
#     if not f.is_file():
#         continue
#
#     try:
#
#         text = f.read_text("ascii")
#         for line in text.splitlines():
#             if line.startswith("0109"):
#                 print(f)
#     except:
#         continue


# with (
#     open(r"C:\Users\ipetrash\Desktop\Visa Base 2\itf\errors\itf_TC54_full_TXI-15493.txt", mode="rb") as f_in,
#     open(r"C:\Users\ipetrash\Desktop\Visa Base 2\itf\errors\itf_TC00_full_TXI-15493.txt", mode="wb") as f_out,
# ):
#     for line in f_in:
#         tc = line[:2]
#         if tc == b"54":
#             tc = b'00'
#         f_out.write(tc + line[2:])
