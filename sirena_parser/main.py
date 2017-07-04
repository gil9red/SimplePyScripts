#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


class SirenaRecord:
    def __init__(self, line):
        self.values = list()
        self.type = line[0]

        data = line[1:]

        import re
        raw = re.split(r'\s+', data)

        for i in range(len(raw)):
            part = raw[i]

            if self.type == '1' and i == 0:
                self.values.append(part[0: 6])
                self.values.append(part[6: 10])
                self.values.append(part[10: 13])
                self.values.append(part[13: 17])
                self.values.append(part[17: 27])
                self.values.append(part[27:])

            elif self.type == '2' and i == 5:
                self.values.append(part[0: 2])
                self.values.append(part[2:])

            elif self.type == '4' and i == 0:
                self.values += part.split("/")

            elif self.type == '6' and i == 0:
                self.values.append(part[0: 6])
                self.values.append(part[6:])

            elif self.type == '7' and i == 0:
                self.values.append(part[0: 6])
                self.values.append(part[6:])

            elif self.type == '9' and (i == 0 or i == 1):
                self.values += part.split("/")

            else:
                self.values.append(part)


class SirenaMessage:
    def __init__(self, queue_lines):
        self.lines = list()
        self.records = list()

        while queue_lines:
            line = queue_lines[0]
            type = line[0]
            if type == 'Z' and self.lines:
                break

            queue_lines.pop(0)
            self.lines.append(line)

            if type in ['9', '1', 'Z']:
                break

        for l in self.lines:
            self.records.append(SirenaRecord(l))


class SirenaFile:
    def __init__(self, file_name):
        self.lines = list()
        self.queue_lines = list()

        self.messages = list()

        with open(file_name, mode='r', encoding='cp1251') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                self.lines.append(line)
                self.queue_lines.append(line)

        self.messages = list()
        while self.queue_lines:
            self.messages.append(SirenaMessage(self.queue_lines))


if __name__ == '__main__':
    in_file_name = 'RET.TCH.STRA.S.20170510-20170510'
    out_file_name = 'parse_RET.TCH.STRA.S.20170510-20170510'

    sirena_file = SirenaFile(in_file_name)

    f = open(out_file_name, 'w', encoding='cp1251', newline='\n')

    for message in sirena_file.messages:
        for record in message.records:
            for value in record.values:
                f.write(value + ";")
                print(value + ";", end='')

            f.write('\n')
            print()

    f.close()
