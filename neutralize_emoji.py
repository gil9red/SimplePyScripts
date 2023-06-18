#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/crinny/gatee/blob/11f78228fbb42dc4e06d180d90974849d4d4e45f/bot/utils/emoji.py#L7


def neutralize_emoji(character: str) -> str:
    """
    Remove skin tone and gender modifiers from the emoji.
    """
    return (
        character.replace("🏻", "")
        .replace("🏼", "")
        .replace("🏽", "")
        .replace("🏾", "")
        .replace("🏿", "")
        .replace("♂️", "")
        .replace("♀️", "")
    )


if __name__ == "__main__":
    text = ", ".join(["👨", "👨🏻", "👨🏼", "👨🏽", "👨🏾", "👨🏿"])
    print(neutralize_emoji(text))
    # 👨, 👨, 👨, 👨, 👨, 👨

    text = ", ".join(["👩", "👩🏻", "👩🏼", "👩🏽", "👩🏾", "👩🏿"])
    print(neutralize_emoji(text))
    # 👩, 👩, 👩, 👩, 👩, 👩
