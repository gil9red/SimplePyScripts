#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://ru.stackoverflow.com/questions/843386/


def timestamp_to_human(time_s):
    items = [
        (31536000, "{} г. "),
        (2592000, "{} мес. "),
        (604800, "{} нед. "),
        (86400, "{} д. "),
        (3600, "{} ч."),
    ]

    if time_s == 0:
        return None

    if time_s < 3600:
        return "меньше часа"

    result = ""

    for value, fmt in items:
        if time_s >= value:
            result += fmt.format(int(time_s / value))
            time_s %= value

    return result


if __name__ == "__main__":
    print(timestamp_to_human(2827567.5759670734))  # 1 мес. 2 д. 17 ч.
    assert timestamp_to_human(2827567.5759670734) == "1 мес. 2 д. 17 ч."

    print(timestamp_to_human(269649.6857390404))  # 3 д. 2 ч.
    assert timestamp_to_human(269649.6857390404) == "3 д. 2 ч."
