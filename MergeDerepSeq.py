#! /Library/Frameworks/Python.framework/Versions/2.7/bin/python

import numpy as np
import os
import sys
import argparse

folder = "SetLength"

#
# Argument
#
parser = argparse.ArgumentParser()
parser.add_argument("-i",dest="inf",action="store",default=".",help="Comma-separated, input files (ex: file1.fasta,file2.fasta,file3.fasta")
parser.add_argument("-o",dest="outf",action="store",default=".",help="Path for output file")
args = parser.parse_args()

##################
# Files
##################
if args.inf != "none" and args.outf != "none":
	files = args.inf.split(",")
	fo = open(args.outf,"w")
else:
	print "Please enter path for input/output files"
	sys.exit()

###
## 
#
seq2id = dict()
seq2num = dict()
for file in files:
	fi = open(file)
	for ii,jj in enumerate(fi):
		if jj[0] == ">":
			if ii != 0:
				if seq2id.has_key(seq): seq2num[seq] += num
				else:
					seq2num[seq] = num
					seq2id[seq] = id
			seq = ""
			line = jj.strip("\n;")
			num = int(line.split(";")[1].split("=")[1])
			id = line.split(";")[0]
		else: seq += jj.strip("\n")
	# last
	seq2num[seq] = num
	seq2id[seq] = id
	fi.close()

seqs = np.array(seq2num.keys())
nums = np.array(seq2num.values())
index = np.argsort(nums)[::-1]
seqs = seqs[index]
for seq in seqs:
	fo.write(seq2id[seq] + ";size=" + str(seq2num[seq]) + ";\n")
	fo.write(seq + "\n")
fo.close()



