#!/usr/bin/python
# -*- coding: utf-8 -*-
from rtree_new import *
from random import uniform
from time import time

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
	data = {}

	queryfile = 'sample1.txt'
	#get dimension on which skylines are to be found and memory blocksize 	
	dims, blocksize = getBlockParametersDimension(queryfile, dims, blocksize)

	inputfile = 'sample_ant.txt'
	
	
	dim = 2
	root = Rtree(m = 3, M = 7)
	n = []

	for i in range(100):
		data = {}
		for j in range(0, dim):
			a = uniform(0, 1000)
			data[j] = a
			data[j+dim] = a
		n.append(node(MBR = data, index = i))
	t0 = time()

	for i in range(100):
		root = Insert(root, n[i])


	print root.findSkylinesStart([1, 2])