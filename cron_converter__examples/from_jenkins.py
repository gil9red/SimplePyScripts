#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re


def do_convert(cron: str) -> str:
    match cron:
        case "@hourly":
            cron = "H * * * *"

        case "@daily" | "@midnight":
            cron = "H 0 * * *"

        case "@weekly":
            cron = "H H * * H"

        case "@monthly":
            cron = "H H H * *"

        case "@yearly" | "@annually":
            cron = "0 0 1 1 *"

    # NOTE: "H(0-29)/10 * * * *" -> "0-29/10 * * * *"
    cron = re.sub(r"H\((.+?)\)", r"\1", cron)

    parts: list[str] = cron.split()

    def _process(value: str, default_value: str = "0") -> str:
        return value.replace("H/", "*/").replace("H", default_value)

    # Minute
    parts[0] = _process(parts[0])

    # Hour
    parts[1] = _process(parts[1])

    # Day (month). Тут диапазон начинается с 1
    parts[2] = _process(parts[2], default_value="1")

    # Month. Тут диапазон начинается с 1
    parts[3] = _process(parts[3], default_value="1")

    # Day (week)
    parts[4] = _process(parts[4])

    cron = " ".join(parts)

    return cron


if __name__ == "__main__":
    from datetime import datetime

    # pip install cron-converter
    from cron_converter import Cron

    cron = "H */8 * * *"
    cron = do_convert(cron)
    cron_instance = Cron(cron)

    print(f"Cron: {cron_instance}")

    start_date = datetime.now()
    print(f"Start date: {start_date}")

    schedule = cron_instance.schedule(start_date)
    print(f"Next: {schedule.next().isoformat()}")
    print(f"Next: {schedule.next().isoformat()}")
    print(f"Next: {schedule.next().isoformat()}")
    print(f"Next: {schedule.next().isoformat()}")
    print(f"Next: {schedule.next().isoformat()}")
