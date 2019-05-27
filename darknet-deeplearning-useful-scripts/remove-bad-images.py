#!/usr/bin/python

import os
import glob

from PIL import Image #pip install Pillow

for f in glob.glob("*.png"):
    try:   
        image = Image.open(f)
        if image.verify() == False:
            raise ValueError('bad img {0}'.format(f))
    except:
        print("{0} looks bad".format(f))
        try:
            os.remove(f)
        except:
            print("{0} looks unremovable".format(f))
			