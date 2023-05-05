#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import enum

from collections import defaultdict
from dataclasses import dataclass
from urllib.parse import urljoin

from bs4 import Tag

from common import parse


URL = "https://eldenring.fandom.com/wiki/Shields"


class ShieldTypeEnum(enum.Enum):
    SMALL = enum.auto()
    MEDIUM = enum.auto()
    GREAT = enum.auto()

    @classmethod
    def parse(cls, shield_type_str: str) -> "ShieldTypeEnum":
        shield_type_str = shield_type_str.lower()
        if "small" in shield_type_str:
            return ShieldTypeEnum.SMALL
        elif "medium" in shield_type_str:
            return ShieldTypeEnum.MEDIUM
        elif "great" in shield_type_str:
            return ShieldTypeEnum.GREAT
        else:
            raise Exception(f"Unknown type {shield_type_str!r}!")


def get_int(value: str) -> int:
    # NOTE: Example: 76.0
    return int(float(value))


@dataclass
class Elements:
    physical: int
    magic: int
    fire: int
    lightning: int
    holy: int

    def total(self) -> int:
        return self.physical + self.magic + self.fire + self.lightning + self.holy


@dataclass
class Attribute:
    scale: str
    required: int


@dataclass
class Attributes:
    strength: Attribute
    dexterity: Attribute
    intelligence: Attribute
    faith: Attribute
    arcane: Attribute


@dataclass
class Shield:
    type: ShieldTypeEnum
    name: str
    url: str
    skill: str
    weight: float
    attack: Elements
    guard: Elements
    attributes: Attributes
    critical: int
    guard_boost: int

    @classmethod
    def parse_from(cls, td_list: list[Tag], type_: ShieldTypeEnum) -> "Shield":
        name = td_list[1].get_text(strip=True)
        url = urljoin(URL, td_list[1].select_one("a[href]")["href"])
        skill = td_list[2].get_text(strip=True)
        weight = float(td_list[3].get_text(strip=True))

        physical_attack, physical_guard = map(
            get_int, td_list[4].get_text(strip=True, separator="\n").split("\n")
        )
        magic_attack, magic_guard = map(
            get_int, td_list[5].get_text(strip=True, separator="\n").split("\n")
        )
        fire_attack, fire_guard = map(
            get_int, td_list[6].get_text(strip=True, separator="\n").split("\n")
        )
        lightning_attack, lightning_guard = map(
            get_int, td_list[7].get_text(strip=True, separator="\n").split("\n")
        )
        holy_attack, holy_guard = map(
            get_int, td_list[8].get_text(strip=True, separator="\n").split("\n")
        )

        critical, guard_boost = map(
            get_int, td_list[9].get_text(strip=True, separator="\n").split("\n")
        )

        strength_scale, strength_required = (
            td_list[10].get_text(strip=True, separator="\n").split("\n")
        )
        dexterity_scale, dexterity_required = (
            td_list[11].get_text(strip=True, separator="\n").split("\n")
        )
        intelligence_scale, intelligence_required = (
            td_list[12].get_text(strip=True, separator="\n").split("\n")
        )
        faith_scale, faith_required = (
            td_list[13].get_text(strip=True, separator="\n").split("\n")
        )
        arcane_scale, arcane_required = (
            td_list[14].get_text(strip=True, separator="\n").split("\n")
        )

        return cls(
            type=type_,
            name=name,
            url=url,
            skill=skill,
            weight=weight,
            attack=Elements(
                physical=physical_attack,
                magic=magic_attack,
                fire=fire_attack,
                lightning=lightning_attack,
                holy=holy_attack,
            ),
            guard=Elements(
                physical=physical_guard,
                magic=magic_guard,
                fire=fire_guard,
                lightning=lightning_guard,
                holy=holy_guard,
            ),
            attributes=Attributes(
                strength=Attribute(strength_scale, get_int(strength_required)),
                dexterity=Attribute(dexterity_scale, get_int(dexterity_required)),
                intelligence=Attribute(
                    intelligence_scale, get_int(intelligence_required)
                ),
                faith=Attribute(faith_scale, get_int(faith_required)),
                arcane=Attribute(arcane_scale, get_int(arcane_required)),
            ),
            critical=critical,
            guard_boost=guard_boost,
        )


def get_shields() -> dict[ShieldTypeEnum, list[Shield]]:
    _, root = parse(URL)

    type_by_shields = defaultdict(list)

    for el_shield_type in root.select("h2:has(.mw-headline)"):
        shield_type_str = el_shield_type.get_text(strip=True)
        shield_type = ShieldTypeEnum.parse(shield_type_str)

        el_table = el_shield_type.find_next_sibling("table")
        for row in el_table.select("tr"):
            td_list = row.select("td")
            if not td_list:
                continue

            type_by_shields[shield_type].append(
                Shield.parse_from(td_list, shield_type)
            )

    return type_by_shields


if __name__ == "__main__":
    type_by_shields = get_shields()
    print(f"Total: {sum(len(v) for v in type_by_shields.values())}")

    print("All shields with guard.physical = 100, sorted by Guard Boost")
    for type_shield, shields in type_by_shields.items():
        shields.sort(key=lambda x: x.guard_boost, reverse=True)

        print(f"{type_shield} ({len(shields)}):")
        for i, shield in enumerate(shields, 1):
            if shield.guard.physical == 100:
                print(f"  {i}. {shield}")

        print()
    """
    ShieldTypeEnum.SMALL (18):
    
    ShieldTypeEnum.MEDIUM (25):
      1. Shield(type=<ShieldTypeEnum.MEDIUM: 2>, name='Brass Shield', url='https://eldenring.fandom.com/wiki/Brass_Shield', skill='', weight=7.0, attack=Elements(physical=84, magic=0, fire=0, lightning=0, holy=0), guard=Elements(physical=100, magic=55, fire=59, lightning=39, holy=54), attributes=Attributes(strength=Attribute(scale='D', required=16), dexterity=Attribute(scale='-', required=0), intelligence=Attribute(scale='-', required=0), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=56)
      2. Shield(type=<ShieldTypeEnum.MEDIUM: 2>, name="Banished Knight's Shield", url='https://eldenring.fandom.com/wiki/Banished_Knight%27s_Shield', skill='', weight=6.0, attack=Elements(physical=81, magic=0, fire=0, lightning=0, holy=0), guard=Elements(physical=100, magic=49, fire=57, lightning=31, holy=48), attributes=Attributes(strength=Attribute(scale='D', required=14), dexterity=Attribute(scale='-', required=0), intelligence=Attribute(scale='-', required=0), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=52)
      3. Shield(type=<ShieldTypeEnum.MEDIUM: 2>, name='Beast Crest Heater Shield', url='https://eldenring.fandom.com/wiki/Beast_Crest_Heater_Shield', skill='Parry', weight=3.5, attack=Elements(physical=77, magic=0, fire=0, lightning=0, holy=0), guard=Elements(physical=100, magic=50, fire=43, lightning=32, holy=42), attributes=Attributes(strength=Attribute(scale='D', required=10), dexterity=Attribute(scale='-', required=0), intelligence=Attribute(scale='-', required=0), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=51)
      4. Shield(type=<ShieldTypeEnum.MEDIUM: 2>, name='Inverted Hawk Heater Shield', url='https://eldenring.fandom.com/wiki/Inverted_Hawk_Heater_Shield', skill='Parry', weight=3.5, attack=Elements(physical=77, magic=0, fire=0, lightning=0, holy=0), guard=Elements(physical=100, magic=49, fire=49, lightning=34, holy=49), attributes=Attributes(strength=Attribute(scale='D', required=10), dexterity=Attribute(scale='-', required=0), intelligence=Attribute(scale='-', required=0), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=50)
      6. Shield(type=<ShieldTypeEnum.MEDIUM: 2>, name='Twinbird Kite Shield', url='https://eldenring.fandom.com/wiki/Twinbird_Kite_Shield', skill='', weight=4.5, attack=Elements(physical=78, magic=0, fire=0, lightning=0, holy=0), guard=Elements(physical=100, magic=49, fire=50, lightning=28, holy=35), attributes=Attributes(strength=Attribute(scale='d', required=12), dexterity=Attribute(scale='-', required=0), intelligence=Attribute(scale='-', required=0), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=49)
      7. Shield(type=<ShieldTypeEnum.MEDIUM: 2>, name='Blue-Gold Kite Shield', url='https://eldenring.fandom.com/wiki/Blue-Gold_Kite_Shield', skill='Parry', weight=5.0, attack=Elements(physical=80, magic=0, fire=0, lightning=0, holy=0), guard=Elements(physical=100, magic=47, fire=53, lightning=35, holy=45), attributes=Attributes(strength=Attribute(scale='d', required=12), dexterity=Attribute(scale='-', required=0), intelligence=Attribute(scale='-', required=0), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=47)
      8. Shield(type=<ShieldTypeEnum.MEDIUM: 2>, name="Carian Knight's Shield", url='https://eldenring.fandom.com/wiki/Carian_Knight%27s_Shield', skill='', weight=4.5, attack=Elements(physical=63, magic=63, fire=0, lightning=0, holy=0), guard=Elements(physical=100, magic=58, fire=28, lightning=19, holy=54), attributes=Attributes(strength=Attribute(scale='D', required=10), dexterity=Attribute(scale='?', required=10), intelligence=Attribute(scale='D', required=15), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=47)
      10. Shield(type=<ShieldTypeEnum.MEDIUM: 2>, name='Kite Shield', url='https://eldenring.fandom.com/wiki/Kite_Shield', skill='', weight=4.5, attack=Elements(physical=78, magic=0, fire=0, lightning=0, holy=0), guard=Elements(physical=100, magic=47, fire=47, lightning=33, holy=47), attributes=Attributes(strength=Attribute(scale='D', required=12), dexterity=Attribute(scale='-', required=0), intelligence=Attribute(scale='-', required=0), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=47)
      11. Shield(type=<ShieldTypeEnum.MEDIUM: 2>, name='Scorpion Kite Shield', url='https://eldenring.fandom.com/wiki/Scorpion_Kite_Shield', skill='Parry', weight=4.5, attack=Elements(physical=78, magic=0, fire=0, lightning=0, holy=0), guard=Elements(physical=100, magic=45, fire=46, lightning=33, holy=50), attributes=Attributes(strength=Attribute(scale='D', required=11), dexterity=Attribute(scale='-', required=0), intelligence=Attribute(scale='-', required=0), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=47)
      12. Shield(type=<ShieldTypeEnum.MEDIUM: 2>, name='Eclipse Crest Heater Shield', url='https://eldenring.fandom.com/wiki/Eclipse_Crest_Heater_Shield', skill='', weight=3.5, attack=Elements(physical=77, magic=0, fire=0, lightning=0, holy=0), guard=Elements(physical=100, magic=44, fire=44, lightning=37, holy=44), attributes=Attributes(strength=Attribute(scale='D', required=10), dexterity=Attribute(scale='-', required=0), intelligence=Attribute(scale='-', required=0), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=46)
      13. Shield(type=<ShieldTypeEnum.MEDIUM: 2>, name='Blue Crest Heater Shield', url='https://eldenring.fandom.com/wiki/Blue_Crest_Heater_Shield', skill='', weight=3.5, attack=Elements(physical=77, magic=0, fire=0, lightning=0, holy=0), guard=Elements(physical=100, magic=43, fire=42, lightning=32, holy=50), attributes=Attributes(strength=Attribute(scale='D', required=10), dexterity=Attribute(scale='-', required=0), intelligence=Attribute(scale='-', required=0), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=44)
      14. Shield(type=<ShieldTypeEnum.MEDIUM: 2>, name='Red Crest Heater Shield', url='https://eldenring.fandom.com/wiki/Red_Crest_Heater_Shield', skill='Parry', weight=3.5, attack=Elements(physical=77, magic=0, fire=0, lightning=0, holy=0), guard=Elements(physical=100, magic=42, fire=50, lightning=32, holy=43), attributes=Attributes(strength=Attribute(scale='D', required=10), dexterity=Attribute(scale='-', required=0), intelligence=Attribute(scale='-', required=0), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=43)
      15. Shield(type=<ShieldTypeEnum.MEDIUM: 2>, name='Albinauric Shield', url='https://eldenring.fandom.com/wiki/Albinauric_Shield', skill='Parry', weight=4.5, attack=Elements(physical=78, magic=0, fire=0, lightning=0, holy=0), guard=Elements(physical=100, magic=61, fire=42, lightning=23, holy=47), attributes=Attributes(strength=Attribute(scale='D', required=11), dexterity=Attribute(scale='-', required=0), intelligence=Attribute(scale='-', required=0), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=42)
      17. Shield(type=<ShieldTypeEnum.MEDIUM: 2>, name='Silver Mirrorshield', url='https://eldenring.fandom.com/wiki/Silver_Mirrorshield', skill='', weight=3.5, attack=Elements(physical=70, magic=45, fire=0, lightning=0, holy=0), guard=Elements(physical=100, magic=89, fire=31, lightning=19, holy=27), attributes=Attributes(strength=Attribute(scale='D', required=12), dexterity=Attribute(scale='?', required=10), intelligence=Attribute(scale='D', required=10), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=42)
      24. Shield(type=<ShieldTypeEnum.MEDIUM: 2>, name='Heater Shield', url='https://eldenring.fandom.com/wiki/Heater_Shield', skill='', weight=3.5, attack=Elements(physical=77, magic=0, fire=0, lightning=0, holy=0), guard=Elements(physical=100, magic=43, fire=43, lightning=27, holy=43), attributes=Attributes(strength=Attribute(scale='D', required=10), dexterity=Attribute(scale='-', required=0), intelligence=Attribute(scale='-', required=0), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=38)
    
    ShieldTypeEnum.GREAT (25):
      1. Shield(type=<ShieldTypeEnum.GREAT: 3>, name='Fingerprint Stone Shield', url='https://eldenring.fandom.com/wiki/Fingerprint_Stone_Shield', skill='Shield Bash', weight=29.0, attack=Elements(physical=158, magic=0, fire=0, lightning=0, holy=0), guard=Elements(physical=100, magic=77, fire=81, lightning=79, holy=75), attributes=Attributes(strength=Attribute(scale='D', required=48), dexterity=Attribute(scale='-', required=0), intelligence=Attribute(scale='-', required=0), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=81)
      2. Shield(type=<ShieldTypeEnum.GREAT: 3>, name='Visage Shield', url='https://eldenring.fandom.com/wiki/Visage_Shield', skill='Tongues of Fire', weight=24.0, attack=Elements(physical=186, magic=0, fire=0, lightning=0, holy=0), guard=Elements(physical=100, magic=62, fire=81, lightning=65, holy=62), attributes=Attributes(strength=Attribute(scale='D', required=24), dexterity=Attribute(scale='-', required=0), intelligence=Attribute(scale='-', required=0), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=75)
      3. Shield(type=<ShieldTypeEnum.GREAT: 3>, name='Golden Greatshield', url='https://eldenring.fandom.com/wiki/Golden_Greatshield', skill='', weight=17.0, attack=Elements(physical=100, magic=0, fire=0, lightning=0, holy=0), guard=Elements(physical=100, magic=57, fire=60, lightning=57, holy=68), attributes=Attributes(strength=Attribute(scale='D', required=34), dexterity=Attribute(scale='-', required=0), intelligence=Attribute(scale='-', required=0), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=68)
      4. Shield(type=<ShieldTypeEnum.GREAT: 3>, name='Haligtree Crest Greatshield', url='https://eldenring.fandom.com/wiki/Haligtree_Crest_Greatshield', skill='', weight=18.5, attack=Elements(physical=116, magic=0, fire=0, lightning=0, holy=0), guard=Elements(physical=100, magic=61, fire=67, lightning=55, holy=79), attributes=Attributes(strength=Attribute(scale='D', required=36), dexterity=Attribute(scale='-', required=0), intelligence=Attribute(scale='-', required=0), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=68)
      5. Shield(type=<ShieldTypeEnum.GREAT: 3>, name='Gilded Greatshield', url='https://eldenring.fandom.com/wiki/Gilded_Greatshield', skill='No Skill', weight=17.5, attack=Elements(physical=115, magic=0, fire=0, lightning=0, holy=0), guard=Elements(physical=100, magic=60, fire=66, lightning=54, holy=65), attributes=Attributes(strength=Attribute(scale='D', required=36), dexterity=Attribute(scale='-', required=0), intelligence=Attribute(scale='-', required=0), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=67)
      6. Shield(type=<ShieldTypeEnum.GREAT: 3>, name='One-Eyed Shield', url='https://eldenring.fandom.com/wiki/One-Eyed_Shield', skill='Flame Spit', weight=20.5, attack=Elements(physical=175, magic=0, fire=0, lightning=0, holy=0), guard=Elements(physical=100, magic=57, fire=69, lightning=59, holy=63), attributes=Attributes(strength=Attribute(scale='D', required=36), dexterity=Attribute(scale='-', required=0), intelligence=Attribute(scale='-', required=0), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=67)
      7. Shield(type=<ShieldTypeEnum.GREAT: 3>, name='Distinguished Greatshield', url='https://eldenring.fandom.com/wiki/Distinguished_Greatshield', skill='', weight=17.0, attack=Elements(physical=112, magic=0, fire=0, lightning=0, holy=0), guard=Elements(physical=100, magic=65, fire=63, lightning=54, holy=60), attributes=Attributes(strength=Attribute(scale='D', required=32), dexterity=Attribute(scale='-', required=0), intelligence=Attribute(scale='-', required=0), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=66)
      8. Shield(type=<ShieldTypeEnum.GREAT: 3>, name='Dragon Towershield', url='https://eldenring.fandom.com/wiki/Dragon_Towershield', skill='Shield Bash', weight=17.5, attack=Elements(physical=115, magic=0, fire=0, lightning=0, holy=0), guard=Elements(physical=100, magic=61, fire=67, lightning=55, holy=64), attributes=Attributes(strength=Attribute(scale='D', required=30), dexterity=Attribute(scale='-', required=0), intelligence=Attribute(scale='-', required=0), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=64)
      9. Shield(type=<ShieldTypeEnum.GREAT: 3>, name='Manor Towershield', url='https://eldenring.fandom.com/wiki/Manor_Towershield', skill='Shield Bash', weight=16.0, attack=Elements(physical=111, magic=0, fire=0, lightning=0, holy=0), guard=Elements(physical=100, magic=66, fire=66, lightning=51, holy=56), attributes=Attributes(strength=Attribute(scale='D', required=30), dexterity=Attribute(scale='-', required=0), intelligence=Attribute(scale='-', required=0), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=64)
      10. Shield(type=<ShieldTypeEnum.GREAT: 3>, name='Crossed-Tree Towershield', url='https://eldenring.fandom.com/wiki/Crossed-Tree_Towershield', skill='Shield Bash', weight=16.0, attack=Elements(physical=111, magic=0, fire=0, lightning=0, holy=0), guard=Elements(physical=100, magic=66, fire=56, lightning=54, holy=66), attributes=Attributes(strength=Attribute(scale='D', required=30), dexterity=Attribute(scale='-', required=0), intelligence=Attribute(scale='-', required=0), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=63)
      11. Shield(type=<ShieldTypeEnum.GREAT: 3>, name='Eclipse Crest Greatshield', url='https://eldenring.fandom.com/wiki/Eclipse_Crest_Greatshield', skill='', weight=15.0, attack=Elements(physical=110, magic=0, fire=0, lightning=0, holy=0), guard=Elements(physical=100, magic=72, fire=57, lightning=51, holy=59), attributes=Attributes(strength=Attribute(scale='D', required=32), dexterity=Attribute(scale='-', required=0), intelligence=Attribute(scale='-', required=0), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=63)
      12. Shield(type=<ShieldTypeEnum.GREAT: 3>, name='Inverted Hawk Towershield', url='https://eldenring.fandom.com/wiki/Inverted_Hawk_Towershield', skill='Shield Bash', weight=16.0, attack=Elements(physical=111, magic=0, fire=0, lightning=0, holy=0), guard=Elements(physical=100, magic=66, fire=56, lightning=54, holy=66), attributes=Attributes(strength=Attribute(scale='D', required=30), dexterity=Attribute(scale='-', required=0), intelligence=Attribute(scale='-', required=0), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=63)
      13. Shield(type=<ShieldTypeEnum.GREAT: 3>, name='Cuckoo Greatshield', url='https://eldenring.fandom.com/wiki/Cuckoo_Greatshield', skill='', weight=15.0, attack=Elements(physical=110, magic=0, fire=0, lightning=0, holy=0), guard=Elements(physical=100, magic=70, fire=56, lightning=52, holy=60), attributes=Attributes(strength=Attribute(scale='D', required=32), dexterity=Attribute(scale='-', required=0), intelligence=Attribute(scale='-', required=0), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=62)
      14. Shield(type=<ShieldTypeEnum.GREAT: 3>, name='Redmane Greatshield', url='https://eldenring.fandom.com/wiki/Redmane_Greatshield', skill='', weight=14.0, attack=Elements(physical=108, magic=0, fire=0, lightning=0, holy=0), guard=Elements(physical=100, magic=54, fire=70, lightning=53, holy=52), attributes=Attributes(strength=Attribute(scale='D', required=30), dexterity=Attribute(scale='-', required=0), intelligence=Attribute(scale='-', required=0), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=61)
      15. Shield(type=<ShieldTypeEnum.GREAT: 3>, name="Ant's Skull Plate", url='https://eldenring.fandom.com/wiki/Ant%27s_Skull_Plate', skill='Shield Bash', weight=13.5, attack=Elements(physical=136, magic=0, fire=0, lightning=0, holy=0), guard=Elements(physical=100, magic=47, fire=42, lightning=57, holy=57), attributes=Attributes(strength=Attribute(scale='D', required=28), dexterity=Attribute(scale='-', required=0), intelligence=Attribute(scale='-', required=0), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=59)
      16. Shield(type=<ShieldTypeEnum.GREAT: 3>, name='Dragonclaw Shield', url='https://eldenring.fandom.com/wiki/Dragonclaw_Shield', skill='Shield Bash', weight=13.5, attack=Elements(physical=118, magic=0, fire=0, lightning=76, holy=0), guard=Elements(physical=100, magic=52, fire=52, lightning=76, holy=47), attributes=Attributes(strength=Attribute(scale='D', required=28), dexterity=Attribute(scale='E', required=12), intelligence=Attribute(scale='-', required=0), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=59)
      17. Shield(type=<ShieldTypeEnum.GREAT: 3>, name='Crucible Hornshield', url='https://eldenring.fandom.com/wiki/Crucible_Hornshield', skill='Shield Bash', weight=11.5, attack=Elements(physical=147, magic=0, fire=0, lightning=0, holy=0), guard=Elements(physical=100, magic=51, fire=50, lightning=46, holy=64), attributes=Attributes(strength=Attribute(scale='D', required=26), dexterity=Attribute(scale='-', required=0), intelligence=Attribute(scale='-', required=0), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=58)
      18. Shield(type=<ShieldTypeEnum.GREAT: 3>, name='Golden Beast Crest Shield', url='https://eldenring.fandom.com/wiki/Golden_Beast_Crest_Shield', skill='', weight=12.5, attack=Elements(physical=104, magic=0, fire=0, lightning=0, holy=0), guard=Elements(physical=100, magic=55, fire=55, lightning=48, holy=55), attributes=Attributes(strength=Attribute(scale='D', required=24), dexterity=Attribute(scale='-', required=0), intelligence=Attribute(scale='-', required=0), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=58)
      19. Shield(type=<ShieldTypeEnum.GREAT: 3>, name='Erdtree Greatshield', url='https://eldenring.fandom.com/wiki/Erdtree_Greatshield', skill='Golden Retaliation', weight=13.5, attack=Elements(physical=120, magic=0, fire=0, lightning=0, holy=78), guard=Elements(physical=100, magic=66, fire=49, lightning=45, holy=76), attributes=Attributes(strength=Attribute(scale='C', required=30), dexterity=Attribute(scale='-', required=0), intelligence=Attribute(scale='-', required=0), faith=Attribute(scale='D', required=12), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=57)
      25. Shield(type=<ShieldTypeEnum.GREAT: 3>, name='Jellyfish Shield', url='https://eldenring.fandom.com/wiki/Jellyfish_Shield', skill='Contagious Rage', weight=8.0, attack=Elements(physical=123, magic=0, fire=0, lightning=0, holy=0), guard=Elements(physical=100, magic=52, fire=52, lightning=40, holy=48), attributes=Attributes(strength=Attribute(scale='D', required=20), dexterity=Attribute(scale='?', required=14), intelligence=Attribute(scale='-', required=0), faith=Attribute(scale='-', required=0), arcane=Attribute(scale='-', required=0)), critical=100, guard_boost=50)
    """
