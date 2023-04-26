#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://www.codewars.com/kata/5ef9ca8b76be6d001d5e1c3e/train/python


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i : i + n]


# Task 1: Encode function
#
# Implement the encode function, using the following steps:
#  - convert every letter of the text to its ASCII value;
#  - convert ASCII values to 8-bit binary;
#  - triple every bit;
#  - concatenate the result;
#
# For example:
#     input: "hey"
#     --> 104, 101, 121                  // ASCII values
#     --> 01101000, 01100101, 01111001   // binary
#     --> 000111111000111000000000 000111111000000111000111 000111111111111000000111  // tripled
#     --> "000111111000111000000000000111111000000111000111000111111111111000000111"  // concatenated
def encode(text: str) -> str:
    return "".join(
        "".join(b * 3 for b in f"{ord(c):08b}") for c in text  # Tripled bits
    )


# Task 2: Decode function:
# Check if any errors happened and correct them. Errors will be only bit flips, and not a loss of bits:
#  - 111 --> 101 : this can and will happen
#  - 111 --> 11 : this cannot happen
#
# Note: the length of the input string is also always divisible by 24 so that you can convert it to an ASCII value.
#
# Steps:
#  - Split the input into groups of three characters;
#  - Check if an error occurred: replace each group with the character that occurs most often,
#    e.g. 010 --> 0, 110 --> 1, etc;
#  - Take each group of 8 characters and convert that binary number;
#  - Convert the binary values to decimal (ASCII);
#  - Convert the ASCII values to characters and concatenate the result
#
# For example:
#     input: "100111111000111001000010000111111000000111001111000111110110111000010111"
#     --> 100, 111, 111, 000, 111, 001, ...  // triples
#     -->  0,   1,   1,   0,   1,   0,  ...  // corrected bits
#     --> 01101000, 01100101, 01111001       // bytes
#     --> 104, 101, 121                      // ASCII values
#     --> "hey"
def decode(bits: str) -> str:
    bit_items = []
    for tripled_bits in chunks(bits, 3):
        sums = sum(map(int, tripled_bits))

        # Example: 110 or 111 -> 1 and 000 -> 0 or 001 -> 0
        bit_items.append("1" if sums == 2 or sums == 3 else "0")

    binary = "".join(bit_items)

    items = []
    for byte in chunks(binary, 8):
        items.append(chr(int(byte, 2)))

    return "".join(items)


if __name__ == "__main__":
    text = "hey"
    encoded = encode(text)
    print(encoded)
    assert (
        encoded
        == "000111111000111000000000000111111000000111000111000111111111111000000111"
    )

    decoded = decode(encoded)
    print(decoded)
    assert text == decoded

    invalid_encoded = "100111111000111001000010000111111000000111001111000111110110111000010111"
    decoded = decode(invalid_encoded)
    print(decoded)
    assert text == decoded
