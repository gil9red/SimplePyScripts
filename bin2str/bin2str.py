#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def bin2str(bin_str: str) -> str:
    # Удаление всех символов кроме 0 и 1
    bin_str = ''.join(c for c in bin_str if c in '01')

    length = len(bin_str)
    if length % 8 != 0:
        raise Exception('Bad length')

    items = []
    for i in range(length // 8):
        end = i * 8 + 8

        b = bin_str[i * 8: end]
        c = chr(int(b, 2))
        items.append(c)

    return ''.join(items)


def str2bin(text: str) -> str:
    bin_words = [bin(ord(c))[2:].rjust(8, '0') for c in text]
    return ' '.join(bin_words)


if __name__ == '__main__':
    assert bin2str('01011001 01101111 01110101') == 'You'
    assert bin2str('010110010110111101110101') == 'You'
    assert bin2str('01011001-01101111-01110101') == 'You'
    assert bin2str('BIN: 01011001-01101111-01110101') == 'You'
    assert str2bin(bin2str('01011001 01101111 01110101')) == '01011001 01101111 01110101'
    assert str2bin(bin2str('010110010110111101110101')) == '01011001 01101111 01110101'

    assert str2bin('You') == '01011001 01101111 01110101'
    assert bin2str(str2bin('You')) == 'You'

    print('Bin to text:')
    text = (
        "01011001 01101111 01110101 00100000 01100001 01110010 01100101 00100000 01101101 01101111 "
        "01110010 01100101 00100000 01110100 01101000 01100001 01101110 00100000 01101010 01110101 "
        "01110011 01110100 00100000 01100001 01101110 00100000 01100001 01101110 01101001 01101101 "
        "01100001 01101100 00101110"
    )
    print(bin2str(text))
    print()

    print('Text to bin:')
    text = "You are more than just an animal."
    print(str2bin(text))
