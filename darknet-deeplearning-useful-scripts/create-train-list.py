import glob
import sys
import os

args = sys.argv[1:]

with open('train.txt', 'w') as the_file:
	for f in glob.glob("{0}/*.png".format(args[0])):
		the_file.write("{0}\n".format(f))
    