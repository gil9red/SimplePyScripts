#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup


session = requests.session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0"


url = "https://www.ign.com/articles/the-best-100-video-games-of-all-time"
rs = session.get(url)
rs.raise_for_status()

root = BeautifulSoup(rs.content, "html.parser")
items = [el.text for el in root.select(".article-page > h2 > strong")]
items.reverse()
print(*items, sep="\n")
assert len(items) == 100
"""
1. The Legend of Zelda: Breath of the Wild
2. Super Mario World
3. Portal 2
4. The Legend of Zelda: A Link to the Past
5. Super Metroid
6. Mass Effect 2
7. Super Mario 64
8. Red Dead Redemption 2
9. Half-Life 2
10. Disco Elysium
11. Super Mario Bros. 3
12. Grand Theft Auto V
13. Hades
14. Castlevania: Symphony of the Night
15. Halo 2
16. The Witcher 3: Wild Hunt
17. The Last of Us
18. BioShock
19. Bloodborne
20. Undertale
21. Super Mario Bros.
22. Street Fighter II
23. Portal
24. Chrono Trigger
25. God of War
26. Half-Life: Alyx
27. Metal Gear Solid 3: Snake Eater
28. Tetris
29. Doom
30. Final Fantasy XIV
31. Half-Life
32. Halo: Combat Evolved
33. Minecraft
34. The Legend of Zelda: Ocarina of Time
35. Sid Meier's Civilization IV
36. Metal Gear Solid
37. Red Dead Redemption
38. The Last of Us Part 2
39. Shadow of the Colossus
40. Resident Evil 4
41. The Elder Scrolls V: Skyrim
42. Metroid Prime
43. Pokémon Yellow
44. Final Fantasy VI
45. Fallout: New Vegas
46. Star Wars: Knights of the Old Republic
47. World of Warcraft
48. StarCraft
49. Diablo II
50. EarthBound
51. Left 4 Dead 2
52. Counter-Strike 1.6
53. Ms. Pac-Man
54. Hollow Knight
55. Apex Legends
56. Overwatch
57. Uncharted 2: Among Thieves
58. Journey
59. The Witness
60. Dishonored 2
61. Batman: Arkham City
62. Rise of the Tomb Raider
63. Call of Duty 4: Modern Warfare
64. Control
65. XCOM 2
66. Grand Theft Auto: San Andreas
67. Silent Hill 2
68. Super Mario World 2: Yoshi's Island
69. Splinter Cell: Chaos Theory
70. The Sims 3
71. Donkey Kong
72. Mario Kart 8 Deluxe
73. Dota 2
74. Return of the Obra Dinn
75. Spelunky 2
76. Super Smash Bros. Ultimate
77. GoldenEye 007
78. Fable 2
79. Fortnite
80. Dark Souls
81. Persona 5 Royal
82. Mortal Kombat 11
83. System Shock 2
84. Resident Evil 2 (Remake)
85. Monster Hunter: World
86. Tony Hawk's Pro Skater 2
87. Titanfall 2
88. Inside
89. SimCity 2000
90. Thief II: The Metal Age
91. Animal Crossing: New Horizons
92. Mega Man 3
93. League of Legends
94. Fallout 2
95. Burnout 3: Takedown
96. Monkey Island 2: LeChuck's Revenge
97. Assassin's Creed IV: Black Flag
98. Final Fantasy VII
99. Divinity: Original Sin 2
100. Borderlands 2
"""
