#! /Library/Frameworks/Python.framework/Versions/2.7/bin/python

import numpy as np
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i",dest="input",action="store",default="",help="Path of input file")
parser.add_argument("-o",dest="output",action="store",default="",help="Path of output file")
parser.add_argument("-short_o",dest="output2",action="store",default="",help="Path of file to write short sequences")
parser.add_argument("-length",type=int,dest="length",action="store",default=100)
parser.add_argument("-truncate",dest="trun",action="store_true",default=False)
args = parser.parse_args()

if args.output2 == "":
	fi = open(args.input)
	fo = open(args.output,"w")
	for ii,jj in enumerate(fi):
		if jj[0] == ">":
			if ii != 0:
				if len(seq) >= args.length:
					fo.write(">" + id + "\n")
					if args.trun: fo.write(seq[:args.length] + "\n")
					else: fo.write(seq + "\n")
				else: print(len(seq))
			seq = ""
			id = jj.strip("\n>")
		else:
			seq += jj.strip("\n")
	if len(seq) >= args.length:
		fo.write(">" + id + "\n")
		if args.trun: fo.write(seq[:args.length] + "\n")
		else: fo.write(seq + "\n")
	fi.close()
	fo.close()
else:
	fi = open(args.input)
	fo = open(args.output,"w")
	fo2 = open(args.output2,"w")
	for ii,jj in enumerate(fi):
		if jj[0] == ">":
			if ii != 0:
				if len(seq) >= args.length:
					fo.write(">" + id + "\n")
					if args.trun: fo.write(seq[:args.length] + "\n")
					else: fo.write(seq + "\n")
				else:
					fo2.write(">" + id + "\n")
					fo2.write(seq + "\n")
			seq = ""
			id = jj.strip("\n>")
		else:
			seq += jj.strip("\n")
	if len(seq) >= args.length:
		fo.write(">" + id + "\n")
		if args.trun: fo.write(seq[:args.length] + "\n")
		else: fo.write(seq + "\n")
	else:
		fo2.write(">" + id + "\n")
		fo2.write(seq + "\n")
	fi.close()
	fo.close()
	fo2.close()

