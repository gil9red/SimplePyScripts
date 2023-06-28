#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import base64
import datetime as DT
import io
import re
import os
import traceback
import winsound

# pip install googletrans
from googletrans import Translator

# pip install pillow
from PIL import ImageGrab

# pip install keyboard
import keyboard

# pip install pytesseract
# tesseract.exe from https://github.com/UB-Mannheim/tesseract/wiki
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def error_sound():
    duration = 300  # milliseconds
    freq = 1000  # Hz
    winsound.Beep(freq, duration)


def run():
    try:
        file_name = f"screenshot_{DT.datetime.now():%Y-%m-%d_%H%M%S}.html"
        print(file_name)

        img = ImageGrab.grab()
        bytes_io = io.BytesIO()
        img.save(bytes_io, img.format)
        img_data = bytes_io.getvalue()

        # Simple image to string
        text = pytesseract.image_to_string(img, lang="eng")
        text = re.sub(r"(\s){2,}", "\1", text)

        translator = Translator()
        translation = translator.translate(text, src="en", dest="ru").text
        print(translation)

        html_text = (
            """
        <body style="width: 100%; height: 100%">
            <table  style="width: 100%; height: 100%">
                <tr>
                    <td colspan="2"><img src="data:image/jpg;base64, {IMAGE_BASE64}" alt="Screenshot" />
                </td></tr>
                <tr>
                    <td><pre>{ORIGINAL_TEXT}</pre></td>
                    <td><pre>{TRANSLATED_TEXT}</td></pre>
                </tr>
            </table>
        </body>
        """.replace(
                "{IMAGE_BASE64}", base64.b64encode(img_data).decode("ascii")
            )
            .replace("{ORIGINAL_TEXT}", text)
            .replace("{TRANSLATED_TEXT}", translation)
        )

        with open(file_name, "w", encoding="utf-8") as f:
            f.write(html_text)

        os.startfile(file_name)

    except Exception as e:
        print(traceback.format_exc())
        error_sound()


keyboard.add_hotkey("Ctrl + 1", run)

keyboard.wait("Ctrl + Q")
