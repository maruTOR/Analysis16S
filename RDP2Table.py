#! /Library/Frameworks/Python.framework/Versions/2.7/bin/python
### ver 1.3 # date: 150123
import numpy as np
import os
import sys
import argparse

parser = argparse.ArgumentParser()
#
parser.add_argument("-i",dest="inf",action="store",type=str,default="none",help="Path for input(output of RDP) file")
parser.add_argument("-o",dest="outf",action="store",type=str,default="none",help="Path for output file")
parser.add_argument("-threshold",dest="threshold",action="store",type=float,default=0.5,help="Threshold (0.5 is encouraged in manual)")
parser.add_argument("-level",dest="level",action="store",type=str,default="Class",help="Taxonomic level (Default:Class)")
parser.add_argument("-other",dest="other",action="store",type=float,default=1,help="Percentage")
parser.add_argument("-undetermined_file",dest="undf",action="store",type=str,default="none",help="Path for file including sequence annotated as undtermined")
parser.add_argument("-seq_file",dest="seqf",action="store",type=str,default="none",help="Path for sequence file. You have to input when you would like to extract undetermined sequence")
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
else:
        print "Please enter path for input/output files"
        sys.exit()
#
target = args.level.lower()
targets = ["domain","phylum","class","order","suborder","family","genus"]
if not target in targets:
	print 'Found something wrong in argument "level". you should input ' + "|".join(targets)
	sys.exit() 

##################
# ReadFile
##################
file2sum = dict()
file2others = dict()
file2undetermined = dict()
file2tax2num = dict()
fnames = []
taxes = []
undetermined_seq_ids = []
tax2num = dict()
for ii,jj in enumerate(fi):
	data = jj.strip("\n").split("\t")
	file = "_".join(data[0].split("_")[1:])
	if not file in fnames: fnames.append(file)
	if target in data:
		index = data.index(target)
		value = float(data[index+1])
		tax = data[index-1].strip('"')
		#
		if value < args.threshold:
			if file2undetermined.has_key(file): file2undetermined[file] += 1
			else: file2undetermined[file] = 1
			undetermined_seq_ids.append(data[0].strip(" "))
		else:
			if not tax in taxes: taxes.append(tax)
			if file2tax2num.has_key(file):
				if file2tax2num[file].has_key(tax): file2tax2num[file][tax] += 1
				else: file2tax2num[file][tax] = 1
			else:
				file2tax2num[file] = dict()
				file2tax2num[file][tax] = 1
for file in fnames:
	if file2undetermined.has_key(file): file2sum[file] = np.sum(file2tax2num[file].values()) + file2undetermined[file]
	else: file2sum[file] = np.sum(file2tax2num[file].values())
fi.close()
#

##################
# tax2props
##################
pers = []; pers2 = []
o_taxes = []
for tax in taxes:
	nums = []
	for fname in fnames:
		if file2tax2num[fname].has_key(tax): nums.append(file2tax2num[fname][tax] / float(file2sum[fname]))
		else: nums.append(0)
	a = sum(nums) / float(len(nums)) * 100
	pers.append(a)
	pers2.append(a)
	if a <= args.other: o_taxes.append(tax)
pers2.sort()
pers2 = np.unique(pers2)
pers2 = pers2[::-1]

##################
# tax2props
##################
fo.write("\t" + "\t".join(fnames) + "\n")
for per in pers2:
	#index = pers.index(per)
	index = np.where(np.array(pers)==per)[0]
	taxes2 = np.unique(np.array(taxes)[index])
	#
	values = []
	for tax in taxes2:
		values = []
		for fname in fnames:
			if tax in o_taxes and file2tax2num[fname].has_key(tax):
				if file2others.has_key(fname): file2others[fname] += file2tax2num[fname][tax]
				else: file2others[fname] = file2tax2num[fname][tax]
			elif file2tax2num[fname].has_key(tax): values.append(str(file2tax2num[fname][tax]))
			else: values.append("0")
		if not tax in o_taxes:
			fo.write(tax + "\t" + "\t".join(values) + "\n")
#
others = []
for fname in fnames:
	if file2others.has_key(fname): others.append(str(file2others[fname]))
	else: others.append("0")
fo.write("Others\t"+ "\t".join(others) + "\n")
undetermines = []
for fname in fnames:
	if file2undetermined.has_key(fname): undetermines.append(str(file2undetermined[fname]))
	else: undetermines.append("0")
fo.write("Undetermined\t"+ "\t".join(undetermines) + "\n")
fo.close()

##################
# Write "undetermined sequence"
##################
if args.seqf != "none" and args.undf != "none":
	fi = open(args.seqf)
	fo = open(args.undf,"w")
	for ii,jj in enumerate(fi):
		if jj[0] == ">":
			id = jj.strip("\n> ")
			if id in undetermined_seq_ids: key = True
			else: key = False
		if key == True:
			fo.write(jj)
	fi.close()
	fo.close()
elif args.undf != "none":
	print "You have to indicate sequence file with -seq_file option"
