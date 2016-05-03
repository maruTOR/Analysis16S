#! /Library/Frameworks/Python.framework/Versions/2.7/bin/python

import numpy as np
import os
import sys
import argparse

#
# Argument
#
parser = argparse.ArgumentParser()
parser.add_argument("-i",dest="inf",action="store",default=".",help="Path for input file")
parser.add_argument("-o",dest="outf",action="store",default=".",help="Path for output file")
parser.add_argument("-rep",dest="rep",action="store",default=False,help="True if you need represent sequence ids")
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

###
## 
#
#
samples = []
otu = 0; otu2sample2nums = dict(); otu2rep = dict()
for ii,jj in enumerate(fi):
	data = jj.strip("\n").split("\t")
	if data[0] == "H":
		if not otu2rep.has_key(data[1]): otu2rep[data[1]] = data[9]
		sample = "_".join(data[8].split("_")[1:])
		if not sample in samples: samples.append(sample)
		if otu2sample2nums.has_key(data[1]):
			if otu2sample2nums[data[1]].has_key(sample): 
				otu2sample2nums[data[1]][sample] += 1
			else:
				otu2sample2nums[data[1]][sample] = 1
		else:
			otu2sample2nums[data[1]] = dict()
			otu2sample2nums[data[1]][sample] = 1
fi.close()
#
samples = np.sort(samples)
if args.rep == True:
	fo.write("OTU\tRepresentSeq\t" + "\t".join(samples) + "\n")
	for i in range(len(otu2sample2nums)):
		otu = str(i)
		vector = np.zeros(len(samples))
		for k in range(len(samples)):
			if otu2sample2nums[otu].has_key(samples[k]):
				vector[k] = otu2sample2nums[otu][samples[k]]
		
		fo.write(str(i+1) + "\t" + otu2rep[otu] + "\t" +  "\t".join(np.array(vector,dtype="S10")) + "\n")
	fo.close()
else:
	fo.write("OTU\t" + "\t".join(samples) + "\n")
	for i in range(len(otu2sample2nums)):
		otu = str(i)
		vector = np.zeros(len(samples))
		for k in range(len(samples)):
			if otu2sample2nums[otu].has_key(samples[k]):
				vector[k] = otu2sample2nums[otu][samples[k]]
		
		fo.write(str(i+1) + "\t" +  "\t".join(np.array(vector,dtype="S10")) + "\n")
	fo.close()
