#! /Library/Frameworks/Python.framework/Versions/2.7/bin/python

import numpy as np
import os 
import sys
import argparse

parser = argparse.ArgumentParser()
#
parser.add_argument("-i",dest="inf",action="store",type=str,default="none",help="List of input file")
parser.add_argument("-o",dest="outf",action="store",type=str,default="none",help="Path for output file")
args = parser.parse_args()

##################
# Files
##################
if args.inf != "none" and args.outf != "none":
	try:
		fi = open(args.inf)
		fo = open(args.outf,"w")
	except IOError:
		print "Cannot recognize the filenames"
	files = []
else:
	print "Please enter path for input/output files"
	sys.exit()

########################
# Load file information
########################
files = []
file2name = dict()
for ii,jj in enumerate(fi):
	data = jj.strip("\n").split("\t")
	files.append(data[0])
	file2name[data[0]] = data[1]
fi.close()

########################
# Make file
########################
for file in files:
	fi = open(file)
	name = file2name[file]
	for ii,jj in enumerate(fi):
		if jj[0] == ">":
			fo.write(jj.strip("\n").split(" ")[0] + "_" + name + "\n")
		else:
			fo.write(jj)
	fi.close()
fo.close()
