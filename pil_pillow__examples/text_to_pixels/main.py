#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PIL import Image, ImageDraw


letters_simbols_nums = [
    'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',
    'z', 'x', 'c', 'v', 'b', 'n', 'm', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S',
    'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ' ', '!', '"', '#', '$',
    '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
    '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', "^", "_", "`", '\n'
]
colors = [
    255, 254, 253, 252, 251, 250, 249, 248, 247, 246, 245, 244, 243, 242, 241, 240, 239, 238, 237, 236, 235, 234,
    233, 232, 231, 230, 229, 228, 227, 226, 225, 224, 223, 222, 221, 220, 219, 218, 217, 216, 215, 214, 213, 212,
    211, 210, 209, 208, 207, 206, 205, 204, 203, 202, 201, 200, 199, 198, 197, 196, 195, 194, 193, 192, 191, 190,
    189, 188, 187, 186, 185, 184, 183, 182, 181, 180, 179, 178, 177, 176, 175, 174, 173, 172, 171, 170, 169, 168,
    167, 166, 165, 164
]

image = Image.new("RGBA", (320, 320), (0, 0, 0, 0))
draw = ImageDraw.Draw(image)

text = """\
Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
sed do eiusmod tempor incididunt ut labore et dolore 
magna aliqua. Ut enim ad minim veniam, quis nostrud 
exercitation ullamco laboris nisi ut aliquip ex ea 
commodo consequat. 
Duis aute irure dolor in reprehenderit in voluptate 
velit esse cillum dolore eu fugiat nulla pariatur. 
Excepteur sint occaecat cupidatat non proident, 
sunt in culpa qui officia deserunt mollit anim id 
est laborum.
"""
items = list(text)

# Подбираем размер, наиболее близкий к длине текста
img_size = -1
for s in range(2, 1000):
    if s * s >= len(items):
        img_size = s
        break

assert img_size != -1, "Не удалось подобрать размер изображения"

image = Image.new("RGBA", (img_size, img_size), (0, 0, 0, 0))
draw = ImageDraw.Draw(image)

for y in range(img_size):
    for x in range(img_size):
        if not items:
            break

        simbol = items.pop(0)
        pos = letters_simbols_nums.index(simbol)
        color = colors[pos]
        draw.point((x, y), fill=(color, 255, 255))

image.save("result.png")
