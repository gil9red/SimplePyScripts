#!/usr/bin/python

import os
import glob

templates = []

print("reading")
for f in glob.glob("*.png"):
    templates.append(int(os.path.basename(f).split('.')[0]))

print("sorting")
templates.sort()

index = templates[0]

print("renaming")
for i in templates:
    try:
        if i != index:
            os.rename('{0}.txt'.format(i), '{0}.txt'.format(index))
            os.rename('{0}.png'.format(i), '{0}.png'.format(index))
    except OSError as err:
        print('bad index {0}'.format(i))
        raise err
    index = index + 1


	
