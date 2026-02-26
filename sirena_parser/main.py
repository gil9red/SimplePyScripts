#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re


class SirenaRecord:
    def __init__(self, line: str) -> None:
        self.values: list[str] = []
        self.type = line[0]

        data = line[1:]
        raw = re.split(r"\s+", data)

        for i, part in enumerate(raw):
            match self.type:
                case "1" if i == 0:
                    self.values.append(part[0:6])
                    self.values.append(part[6:10])
                    self.values.append(part[10:13])
                    self.values.append(part[13:17])
                    self.values.append(part[17:27])
                    self.values.append(part[27:])

                case "2" if i == 5:
                    self.values.append(part[0:2])
                    self.values.append(part[2:])

                case "4" if i == 0:
                    self.values += part.split("/")

                case "6" if i == 0:
                    self.values.append(part[0:6])
                    self.values.append(part[6:])

                case "7" if i == 0:
                    self.values.append(part[0:6])
                    self.values.append(part[6:])

                case "9" if i in [0, 1]:
                    self.values += part.split("/")

                case _:
                    self.values.append(part)


class SirenaMessage:
    def __init__(self, queue_lines: list[str]) -> None:
        self.lines: list[str] = []
        self.records: list[SirenaRecord] = []

        while queue_lines:
            line = queue_lines[0]
            type = line[0]
            if type == "Z" and self.lines:
                break

            queue_lines.pop(0)
            self.lines.append(line)

            if type in ["9", "1", "Z"]:
                break

        for l in self.lines:
            self.records.append(
                SirenaRecord(l)
            )


class SirenaFile:
    def __init__(self, file_name: str) -> None:
        self.lines: list[str] = []
        self.queue_lines: list[str] = []
        self.messages: list[SirenaMessage] = []

        with open(file_name, encoding="cp1251") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                self.lines.append(line)
                self.queue_lines.append(line)

        while self.queue_lines:
            self.messages.append(SirenaMessage(self.queue_lines))


if __name__ == "__main__":
    in_file_name = "RET.TCH.STRA.S.20170510-20170510"
    out_file_name = "parse_RET.TCH.STRA.S.20170510-20170510"

    sirena_file = SirenaFile(in_file_name)

    with open(out_file_name, "w", encoding="cp1251", newline="\n") as f:
        for message in sirena_file.messages:
            for record in message.records:
                for value in record.values:
                    f.write(value + ";")
                    print(value + ";", end="")

                f.write("\n")
                print()
