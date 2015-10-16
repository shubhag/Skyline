#!/usr/bin/python
# -*- coding: utf-8 -*-
from rtree_new import *
from random import uniform
from time import time
import heapq
data = {}

dim = 2
# for i in range(100000):
#     # x = uniform(-1000, 1000)
#     # y = uniform(-1000, 1000)
#     # data[i] = [None]*(2*dim)
#     for j in range(0, dim):
#     	a = uniform(-1000, 1000)
#     	data[i][j] = a
#     	data[i][j+dim] = a + 0.01 
#     # data[i] = {'xmin':x, 'xmax':x + 0.01, 'ymin':y, 'ymax':y + 0.01}

root = Rtree(m = 3, M = 7)
n = []

for i in range(100000):
	data = []
	for j in range(0, dim):
		a = uniform(-1000, 1000)
		data[j] = a
		data[j+dim] = a + 0.01
	print data
	n.append(node(MBR = data, index = i))
t0 = time()

for i in range(100000):
    root = Insert(root, n[i])
# t1 = time()

# print 'Inserting ...'
# print t1 - t0

# x = root.Search(merge(n[0].MBR, n[1].MBR))
# t2 = time()
# print 'Searching ...'
# print t2 - t1


priorityQ = []
