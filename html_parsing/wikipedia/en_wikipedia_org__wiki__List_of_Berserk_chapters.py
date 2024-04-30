#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re

from bs4 import BeautifulSoup
from common import session


def get_chapters() -> list[str]:
    url = "https://en.wikipedia.org/wiki/List_of_Berserk_chapters"

    rs = session.get(url)
    rs.raise_for_status()

    soup = BeautifulSoup(rs.content, "html.parser")

    items = []
    for li in soup.select("li"):
        text = li.get_text(strip=True)
        if re.search(r"^\d+(–\d+)?\.", text):
            items.append(text)

    if not items:
        raise Exception("Chapters is not found!")

    return items


if __name__ == "__main__":
    chapters = get_chapters()
    print(f"Chapters ({len(chapters)}):")
    print(*chapters[:5], sep="\n")
    print("...")
    print(*chapters[-5:], sep="\n")
    """
    Chapters (321):
    001. "Sword Wind"(剣風,Kenpū)
    002–005. "Nosferatu Zodd (1–4)"(不死の（ノスフェラトゥ）ゾッド(1〜4),Nosuferatu Zoddo (1–4))
    006. "Master of the Sword (1)"(剣の主(1),Tsurugi no Aruji (1))
    007. "Master of the Sword (2)"(剣の主(2),Tsurugi no Aruji (2))
    008–011. "Assassin (1–4)"(暗殺者(1〜4),Ansatsusha (1–4))
    ...
    373. "Rusted Iron Bands Unable to Push On"(歩みかなわぬ錆びた鉄輪,Ayumi Kanawanu Sabita Kanawa)
    083. "God of the Abyss (2)"(深淵の神(2),Shin'en no Kami (2), omitted from volume 13)
    374. "Is the Sleeping Black Beast But Biding its Time?"(眠れる黒の獣はただ静かに佇むのか,Nemureru Kuro no Kemono wa Tada Shizuka ni Tatazumu no Ka)
    375. "Dawn Breaks on the Unyielding Fog of Night"(晴れぬ夜霧の朝まだき,Harenu Yogiri no Asamadaki)
    376. "Sea's Quivering Surface and Calamitous War's Shadow"(震える海面と悲惨な戦争の影,Furueru Kaimen to Hisan'na Sensō no Kage)
    """
