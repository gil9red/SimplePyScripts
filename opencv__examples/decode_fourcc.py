#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def decode_fourcc(v) -> str:
    v = int(v)
    return "".join(chr((v >> 8 * i) & 0xFF) for i in range(4))


if __name__ == "__main__":
    assert decode_fourcc(828601953) == "avc1"

    import cv2
    assert decode_fourcc(cv2.VideoWriter_fourcc(*"XVID")) == "XVID"
    assert decode_fourcc(cv2.VideoWriter_fourcc(*"avc1")) == "avc1"
