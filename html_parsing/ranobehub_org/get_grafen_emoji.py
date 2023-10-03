#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from common import session


def get_grafen_emoji() -> list[dict[str, str]]:
    rs = session.get("https://ranobehub.org/api/emoji")
    rs.raise_for_status()

    return rs.json()["data"]


if __name__ == "__main__":
    items = get_grafen_emoji()
    print(f"Items ({len(items)}):")
    for i, x in enumerate(items, 1):
        name, emoji = x['name'], x['emoji']
        print(f"{i}. {name}: {emoji}")
    """
    1. grafen:grafen:is_dead: https://ranobehub.org/api/media/65851
    2. mirkano:mirkano:hotgirl: https://ranobehub.org/api/media/97456
    3. discord:discord:fun_girl: https://ranobehub.org/api/media/102589
    4. discord:discord:oh_yeah_girl: https://ranobehub.org/api/media/104215
    5. discord:discord:pepe_oh_god: https://ranobehub.org/api/media/104216
    6. discord:discord:garold: https://ranobehub.org/api/media/104217
    7. discord:discord:drink: https://ranobehub.org/api/media/104218
    8. discord:discord:wat: https://ranobehub.org/api/media/104219
    9. discord:discord:dogma: https://ranobehub.org/api/media/104220
    10. discord:discord:pico_wat: https://ranobehub.org/api/media/104221
    11. discord:discord:the_lich: https://ranobehub.org/api/media/104222
    12. discord:discord:cat_scream: https://ranobehub.org/api/media/104224
    13. discord:discord:cute-cat: https://ranobehub.org/api/media/109733
    14. discord:discord:funny-girl: https://ranobehub.org/api/media/109734
    15. discord:discord:f-moment: https://ranobehub.org/api/media/109735
    16. discord:discord:haha-meme: https://ranobehub.org/api/media/109736
    17. discord:discord:sad-meme: https://ranobehub.org/api/media/109737
    18. discord:discord:cat-wtf: https://ranobehub.org/api/media/130926
    19. discord:discord:pepe: https://ranobehub.org/api/media/160645
    20. discord:discord:fuck: https://ranobehub.org/api/media/160646
    21. discord:discord:aqua: https://ranobehub.org/api/media/160648
    22. discord:discord:ancient_guy: https://ranobehub.org/api/media/160649
    23. discord:discord:whatwhat: https://ranobehub.org/api/media/160650
    24. discord:discord:monkey: https://ranobehub.org/api/media/160651
    25. discord:discord:oh-boy: https://ranobehub.org/api/media/160652
    26. discord:discord:likelikelike: https://ranobehub.org/api/media/160653
    27. anime:anime:okay-girl: https://ranobehub.org/api/media/298820
    28. anime:anime:friends: https://ranobehub.org/api/media/298821
    29. anime:anime:ohhh: https://ranobehub.org/api/media/298822
    30. anime:anime:ohhhhhh-horny: https://ranobehub.org/api/media/298823
    31. anime:anime:friends2: https://ranobehub.org/api/media/298825
    32. anime:anime:fucku: https://ranobehub.org/api/media/298826
    33. anime:anime:fuck: https://ranobehub.org/api/media/298828
    34. anime:anime:angry: https://ranobehub.org/api/media/298829
    35. anime:anime:ban: https://ranobehub.org/api/media/298830
    36. anime:anime:cool: https://ranobehub.org/api/media/298831
    37. anime:anime:bruh: https://ranobehub.org/api/media/298832
    38. anime:anime:cry: https://ranobehub.org/api/media/298833
    39. anime:anime:disgusting: https://ranobehub.org/api/media/298834
    40. anime:anime:gun: https://ranobehub.org/api/media/298835
    41. anime:anime:hello: https://ranobehub.org/api/media/298836
    42. anime:anime:hmm: https://ranobehub.org/api/media/298837
    43. anime:anime:kek: https://ranobehub.org/api/media/298838
    44. anime:anime:kek2: https://ranobehub.org/api/media/298839
    45. anime:anime:love: https://ranobehub.org/api/media/298840
    46. anime:anime:lurk: https://ranobehub.org/api/media/298841
    47. anime:anime:nice: https://ranobehub.org/api/media/298842
    48. anime:anime:omg: https://ranobehub.org/api/media/298843
    49. anime:anime:home: https://ranobehub.org/api/media/298844
    50. anime:anime:pressf: https://ranobehub.org/api/media/298845
    51. anime:anime:sad: https://ranobehub.org/api/media/298846
    52. anime:anime:socute: https://ranobehub.org/api/media/298847
    53. anime:anime:tea: https://ranobehub.org/api/media/298848
    54. anime:anime:think: https://ranobehub.org/api/media/298849
    55. anime:anime:triggered: https://ranobehub.org/api/media/298850
    """
