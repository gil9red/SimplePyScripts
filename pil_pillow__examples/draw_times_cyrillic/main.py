#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://ru.stackoverflow.com/q/1236348/201445


from PIL import ImageFont, Image, ImageDraw


PADDING = 25
LINE_SIZE = 2
BOTTOM_PADDING = 150
FONTS = "fonts"


def set_text(template, texts):
    font_upper = ImageFont.truetype(f"{FONTS}/times.ttf", 64)
    font_lower = ImageFont.truetype(f"{FONTS}/times.ttf", 46)

    draw_upper_text = ImageDraw.Draw(template)
    upper_text_width, _ = draw_upper_text.textsize(texts[0], font_upper)
    draw_upper_text.text(
        (
            (template.width-upper_text_width)/2,
            template.height-BOTTOM_PADDING+10
        ),
        texts[0], fill="white", font=font_upper
    )

    draw_lower_text = ImageDraw.Draw(template)
    lower_text_width, _ = draw_lower_text.textsize(texts[1], font_lower)
    draw_lower_text.text(
        (
            (template.width-lower_text_width)/2,
            template.height-BOTTOM_PADDING+(PADDING*4)-10
        ),
        texts[1], fill="white", font=font_lower
    )
    return template


if __name__ == '__main__':
    img = Image.new("RGB", (400, 300), "black")

    set_text(img, ["ПРИВЕТ", "HELLO WORLD!"])

    img.show()
