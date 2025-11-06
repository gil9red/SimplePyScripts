#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
from pathlib import Path


DIR = Path(__file__).parent.resolve()
path_output = DIR / "tc33a-all-files.txt"

with open(path_output, "w", encoding="ascii") as f_out:
    path_dir = Path(r"C:\DOC\Visa спецификации\Base II TC33A\TC33_Capture_Transaction")
    for f in path_dir.rglob("*.*"):
        if not f.is_file():
            print(f"[#] Не файл: {str(f)!r}")
            continue

        if any(
            name in str(f)
            for name in [
                # NOTE: Замечены файлы с кривым форматом, типа дат 222222 и 123456.
                #       В задаче не было таких, вероятно кривой пример
                "TWICH-4378",
                # NOTE: Файл был дополнен, переделан и отдельно занесен в тест
                "TC33_CaptureTran_All_CP_Test.ctf",
                # NOTE: Была ошибка при парсинге, постфикс имени файла вызывает сомнения
                "TC33_CaptureTran_All_CP_Test (No CP07, CP05 TCR7)_VISA_err.ctf",
            ]
        ):
            print(f"[#] Пропуск файла: {str(f)!r}")
            continue

        print(f)
        print(f.relative_to(path_dir))

        try:
            text: str = f.read_text("ascii")
            print("Длина:", len(text))

            first_line_length = len(text.splitlines()[0])
            print("Длина первой строки:", first_line_length)
            if first_line_length != 168:
                print("[#] Не CTF, пропуск файла")
                continue

            # NOTE: Кривой формат даты
            if "_MC" in str(f) and "CP12" in text and "12345678  " in text:
                print(f"[#] Замена кривой даты в {str(f)!r}")
                text = text.replace("12345678  ", "1030140815")

            if "inctf TC33A.EPIN.txt" in str(f) and "262012" in text:
                print(f"[#] Замена кривой даты в {str(f)!r}")
                text = text.replace("262012", "261220")

            lines = text.splitlines()
            for i, line in enumerate(lines):
                if line.startswith("3301") and re.search("^3300.+?CP06", lines[i - 1]):
                    print(
                        f"[#] Комментирование строки CP06 TCR1 - не поддерживается запись"
                    )
                    lines[i] = f"# NOTE: Not supported: {line}"

                elif line.startswith("3309170"):
                    print(
                        f"[#] Комментирование строки CP01 TCR9 - не поддерживается запись"
                    )
                    lines[i] = f"# NOTE: Not supported: {line}"

            text = "\n".join(lines)

            f_out.write(f"# START FILE: {f.relative_to(path_dir)}\n")
            f_out.write(text)
            f_out.write(f"\n# END FILE: {f.relative_to(path_dir)}\n\n")

        except UnicodeDecodeError as e:
            print("[#]", e)

        print()
