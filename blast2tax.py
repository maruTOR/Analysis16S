#! /Library/Frameworks/Python.framework/Versions/2.7/bin/python

## parse blast result against SILVA Database

import numpy as np
import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-blast",dest="input1",action="store",default="",help="Path of input file")
parser.add_argument("-id2tax",dest="input2",action="store",default="",help="Path of input file")
parser.add_argument("-all",dest="all",action="store_true",default=False,help="Extract all hits")
parser.add_argument("-o",dest="output",action="store",default="",help="Path of output file")
args = parser.parse_args()

#
# parameters
#
if args.input1 != "" and args.input2 != "" and args.output != "":
	try:
		fi1 = open(args.input1)
		fi2 = open(args.input2)
		fo = open(args.output,"w")
	except IOError:
		print "Cannot recognize filenames"
		sys.exit()
else:
	print "Please indicate input/output files"
	sys.exit()

id2tax = dict()
for ii,jj in enumerate(fi2):
	data = jj.strip("\n").split("\t")
	id2tax[data[0]] = "\t".join(data[1:])
fi2.close()

id = ""
if args.all:
	for ii,jj in enumerate(fi1):
		data = jj.strip("\n").split("\t")
		if id != data[0]:
			evalue = float(data[10])
			tax = id2tax[data[1]]
			fo.write(data[0] + "\t" + data[2] + "\t" + tax + "\n")
			id = data[0]
		elif evalue == float(data[10]):
			tax = id2tax[data[1]]
			fo.write(data[0] + "\t" + data[2] + "\t" + tax + "\n")
			id = data[0]
else:
	for ii,jj in enumerate(fi1):
		data = jj.strip("\n").split("\t")
		if id != data[0]:
			tax = id2tax[data[1]]
			fo.write(data[0] + "\t" + data[2] + "\t" + tax + "\n")
			id = data[0]
fi1.close()
fo.close()
