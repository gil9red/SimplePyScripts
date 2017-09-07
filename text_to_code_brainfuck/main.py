#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def text_to_code_brainfuck(text):
    commands_brainfuck = []

    for c in text:
        commands_brainfuck.append('+' * ord(c) + '.')

    return '>'.join(commands_brainfuck)


if __name__ == '__main__':
    text = 'Hello World!'
    # text = """\
    # #include <iostream>
    # #include <fstream>
    # #include <vector>
    #
    # using namespace std;
    #
    # static char cpu[30000];
    #
    # int main(int argc, char **argv) {
    #     vector<char> acc;
    #     char ch;
    #     ifstream infile(argv[1]);
    #     while (infile) {
    #         infile.get(ch);
    #         acc.push_back(ch);
    #     }
    #     infile.close();
    #     unsigned int j = 0;
    #     int brc = 0;
    #     for (int i = 0; i < acc.size(); ++i) {
    #         if (acc[i] == '>')
    #             j++;
    #         if (acc[i] == '<')
    #             j--;
    #         if (acc[i] == '+')
    #             cpu[j]++;
    #         if (acc[i] == '-')
    #             cpu[j]--;
    #         if (acc[i] == '.')
    #             cout << cpu[j];
    #         if (acc[i] == ',')
    #             cin >> cpu[j];
    #         if (acc[i] == '[') {
    #             if (!cpu[j]) {
    #                 ++brc;
    #                 while (brc) {
    #                     ++i;
    #                     if (acc[i] == '[')
    #                         ++brc;
    #                     if (acc[i] == ']')
    #                         --brc;
    #                 }
    #             } else
    #                 continue;
    #         } else if (acc[i] == ']') {
    #             if (!cpu[j])
    #                 continue;
    #             else {
    #                 if (acc[i] == ']')
    #                     brc++;
    #                 while (brc) {
    #                     --i;
    #                     if (acc[i] == '[')
    #                         brc--;
    #                     if (acc[i] == ']')
    #                         brc++;
    #                 }
    #                 --i;
    #             }
    #         }
    #     }
    # }
    # """

    code_brainfuck = text_to_code_brainfuck(text)
    print(len(code_brainfuck))
    # print(code_brainfuck)

    with open('code.bf', mode='w', encoding='utf-8') as f:
        f.write(code_brainfuck)
