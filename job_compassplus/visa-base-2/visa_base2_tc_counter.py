#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from collections import Counter
from pathlib import Path


# TODO: argparser
DIR = Path(r"C:\Users\ipetrash\Desktop\IMPORT_EXPORT\Visa Base 2")

for path in DIR.rglob("*"):
    if not path.is_file() or "errors" in str(path):
        continue

    print(path)

    tc_by_counter = Counter()
    tc_tcr_by_counter = Counter()

    with open(path, "rb") as f:
        for line in f:
            is_ctf: bool = len(line.rstrip(b"\n\r")) == 168  # TODO: Возможно просто "\n"
            tc_raw: bytes = line[:2]
            tcr_raw: bytes = line[3:4] if is_ctf else line[5:6]
            # TODO: Support EBCDIC, example b'\xf9\xf0' -> 90
            #       Нужно проверить и использовать кодировку cp500
            try:
                tc: str = tc_raw.decode("ascii")
            except UnicodeDecodeError as e:
                print(f"    [#] Skip. Error on {tc_raw}: {e}")
                break

            try:
                tcr: str = tcr_raw.decode("ascii")
            except UnicodeDecodeError as e:
                print(f"    [#] Skip. Error on {tcr_raw}: {e}")
                break

            if not tc.strip() or tc in ["90", "91", "92", "00"]:
                continue

            tc_by_counter[tc] += 1
            tc_tcr_by_counter[f"{tc}-{tcr}"] += 1

    print("    TC:     " + ", ".join(f"{k}: {v}" for k, v in tc_by_counter.items()))
    print("    TC-TCR: " + ", ".join(f"{k}: {v}" for k, v in tc_tcr_by_counter.items()))
