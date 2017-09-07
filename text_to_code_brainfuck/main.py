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
#     text = """\
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
#     """

    code_brainfuck = text_to_code_brainfuck(text)
    print('code_brainfuck:', len(code_brainfuck))
    # print(code_brainfuck)
    print()

    # Test generated brainfuck code
    import simple_brainfuck
    result = simple_brainfuck.execute(code_brainfuck)
    print('result:', len(result))
    print(result)
    assert result == text

    # TODO: Compress variant
    import zlib
    code_brainfuck_compress = zlib.compress(code_brainfuck.encode('utf-8'))
    print()
    print('code_brainfuck_compress:', len(code_brainfuck_compress))
    print(code_brainfuck_compress)

    import base64
    code_brainfuck_compress_base64 = base64.b64encode(code_brainfuck_compress).decode('utf-8')
    print()
    print('code_brainfuck_compress_base64:', len(code_brainfuck_compress_base64))
    print(code_brainfuck_compress_base64)

    with open('code.bf', mode='w', encoding='utf-8') as f:
        f.write(code_brainfuck)
