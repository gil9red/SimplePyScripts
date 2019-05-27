#!/usr/bin/python

import os
import glob


from PIL import Image #pip install Pillow

for f in glob.glob("*.txt"):

	img = str(f.split('.')[0])+".png"
	
	if os.path.isfile(img) == False:
		print("{0} bad".format(f))
		os.remove(f)
