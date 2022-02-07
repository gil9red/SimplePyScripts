#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import requests
from bs4 import BeautifulSoup


session = requests.session()
session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'


url = 'https://www.ign.com/articles/the-best-100-video-games-of-all-time'
rs = session.get(url)
rs.raise_for_status()

root = BeautifulSoup(rs.content, 'html.parser')
items = [
    el.text
    for el in root.select('.article-page > h2 > strong')
]
print(*items, sep='\n')
assert len(items) == 100
"""
100. Borderlands 2
99. Divinity: Original Sin 2
98. Final Fantasy VII
97. Assassin's Creed IV: Black Flag
96. Monkey Island 2: LeChuck's Revenge
95. Burnout 3: Takedown
94. Fallout 2
93. League of Legends
92. Mega Man 3
91. Animal Crossing: New Horizons
90. Thief II: The Metal Age
89. SimCity 2000
88. Inside
87. Titanfall 2
86. Tony Hawk's Pro Skater 2
85. Monster Hunter: World
84. Resident Evil 2 (Remake)
83. System Shock 2
82. Mortal Kombat 11
81. Persona 5 Royal
80. Dark Souls
79. Fortnite
78. Fable 2
77. GoldenEye 007
76. Super Smash Bros. Ultimate
75. Spelunky 2
74. Return of the Obra Dinn
73. Dota 2
72. Mario Kart 8 Deluxe
71. Donkey Kong
70. The Sims 3
69. Splinter Cell: Chaos Theory
68. Super Mario World 2: Yoshi's Island
67. Silent Hill 2
66. Grand Theft Auto: San Andreas
65. XCOM 2
64. Control
63. Call of Duty 4: Modern Warfare
62. Rise of the Tomb Raider
61. Batman: Arkham City
60. Dishonored 2
59. The Witness
58. Journey
57. Uncharted 2: Among Thieves
56. Overwatch
55. Apex Legends
54. Hollow Knight
53. Ms. Pac-Man
52. Counter-Strike 1.6
51. Left 4 Dead 2
50. EarthBound
49. Diablo II
48. StarCraft
47. World of Warcraft
46. Star Wars: Knights of the Old Republic
45. Fallout: New Vegas
44. Final Fantasy VI
43. Pokémon Yellow
42. Metroid Prime
41. The Elder Scrolls V: Skyrim
40. Resident Evil 4
39. Shadow of the Colossus
38. The Last of Us Part 2
37. Red Dead Redemption
36. Metal Gear Solid
35. Sid Meier's Civilization IV
34. The Legend of Zelda: Ocarina of Time
33. Minecraft
32. Halo: Combat Evolved
31. Half-Life
30. Final Fantasy XIV
29. Doom
28. Tetris
27. Metal Gear Solid 3: Snake Eater
26. Half-Life: Alyx
25. God of War
24. Chrono Trigger
23. Portal
22. Street Fighter II
21. Super Mario Bros.
20. Undertale
19. Bloodborne
18. BioShock
17. The Last of Us
16. The Witcher 3: Wild Hunt
15. Halo 2
14. Castlevania: Symphony of the Night
13. Hades
12. Grand Theft Auto V
11. Super Mario Bros. 3
10. Disco Elysium
9. Half-Life 2
8. Red Dead Redemption 2
7. Super Mario 64
6. Mass Effect 2
5. Super Metroid
4. The Legend of Zelda: A Link to the Past
3. Portal 2
2. Super Mario World
1. The Legend of Zelda: Breath of the Wild
"""
