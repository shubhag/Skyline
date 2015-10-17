#!/usr/bin/python
# -*- coding: utf-8 -*-
from rtree_new import *
from random import uniform
import time

def getBlockParametersDimension(queryfile, dims, blocksize):
	query = open(queryfile, 'r')
	line1 = query.readline().rstrip()
	dims = line1.split('\t')
	dims = map(int, dims)
	line2 = query.readline().rstrip()
	blocksize = int (line2)
	query.close()
	return dims, blocksize

if __name__ == '__main__':
	startTime = time.time()
	data = {}

	#get dimension on which skylines are to be found and memory blocksize 	
	queryfile = 'sample_query.txt'
	dims = []
	blocksize  = 0
	dims, blocksize = getBlockParametersDimension(queryfile, dims, blocksize)
	root = Rtree(m = blocksize/2, M = blocksize)

	#get input file of objects
	infilename = 'sample_ind.txt'
	outfilename = 'output_ind.txt'
	inputfile = open(infilename, 'r')
	n = []
	for line in inputfile:
		line = line.rstrip().lstrip()
		words = line.split('\t')
		obj = words[1:]
		obj = map(float, obj)		#converts string list to int list
		index = int (words[0])
		data = {}
		d = len(obj)
		for j in range(0, d):
			data[j] = obj[j]
			data[j+d] = obj[j]
		n.append(node(MBR = data, index = index))
	inputfile.close()

	for i in range(0, len(n)):
		root = Insert(root, n[i])

	comparisons = 0
	skylines, comparisons = root.findSkylinesStart(dims)

	skyIndex = []
	for obj in skylines:
		skyIndex.append(obj[0])
	skyIndex = sorted(skyIndex)
	endTime = time.time()

	#print results
	outfile = open(outfilename, 'w')
	outfile.write("Total running time: "+ str(endTime - startTime) + " sec\n")
	outfile.write("Comparisons: "+ str(comparisons)+"\n")
	outfile.write("Size of skyline set: "+str(len(skyIndex)) + "\n")
	outfile.write("Ids of the skyline objects: \n")
	outfile.write(str(skyIndex))
	outfile.write("\n")
	outfile.close()