#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path

from common import session
from get_reactions import get_reactions_raw


PATH = Path(__file__)
DIR = PATH.parent.resolve()

DIR_IMAGES = DIR / f"{PATH.name}_images"
DIR_IMAGES.mkdir(exist_ok=True, parents=True)


def download_reaction_images(url: str, dir_path: Path = DIR_IMAGES) -> None:
    for x in get_reactions_raw(url)["reactions"]:
        img_url = x["reaction"]["image"]

        rs = session.get(img_url)
        rs.raise_for_status()

        name = x["reaction"]["name"]
        img_suffix = Path(img_url).suffix

        img_path = dir_path / f"{name}{img_suffix}"
        img_path.write_bytes(rs.content)


if __name__ == "__main__":
    download_reaction_images("https://ranobehub.org/ranobe/72/1/1")
