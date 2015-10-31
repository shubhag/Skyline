#!/usr/bin/python

import heapq
from random import uniform
import time
import math

def contain(MBR1, MBR2):
	d = len(MBR1)/2
	for i in range(0,d):
		if MBR1[i] > MBR2[i]:
			return 0
	for i in range(0,d):
		if MBR1[i+d] < MBR2[i+d]:
			return 0
	return 1

#merges 2 bounding rectangles
def merge(MBRa, MBRb):
	if len(MBRa) == 0 :
		return MBRb
	if len(MBRb) == 0 :
		return MBRa

	#intialise MBR
	MBR = []
	dimension = len(MBRa)/2

	for i in range(0, d):
		MBR.append(min(MBRa[i], MBRb[i]))

	for i in range(d, 2*d):
		MBR.append(max(MBRa[i], MBRb[i]))

	return MBR	

def insert(root, Node):
	target = root.selectLeaf(Node)
	Node.parent = target
	target.leaves.append(Node)
	target.MBR = merge(target.MBR, Node.MBR)
	target.AdjustTree()
	if root.parent != None:
		root = root.parent
	return root

def notDominated(skylineSet, MBR, dims):
	global comparisons
	for skyline in skylineSet:
		comparisons += 1
		if dominating(skyline[1], MBR, dims):
			return False
	return True

def dominating(obj1, obj2, dims):
	for i in dims:
		index = i - 1
		if obj1[index] > obj2[index]:
			return False
	return True

def increaseVolume(MBR1, MBR2):
	d = len(MBR1)/2 
	currSpace = 1.0
	for i in range(0,d):
		currSpace = currSpace * (MBR1[i+d] - MBR1[i])

	newSpace = 1.0
	for i in range(0,d):
		newSpace = newSpace * (max(MBR1[i+d], MBR2[i+d]) - min(MBR1[i], MBR2[i]))

	return newSpace - currSpace   

def getSpace(MBR):
	d = len(MBR)/2 
	space = 1.0
	for i in range(0,d):
		space = space * (MBR[i+d] - MBR[i])
	return space

def indexingValue(MBR, dims):
	# d = len(MBR)/2
	indexValue = 0
	for i in dims:
		j = i - 1
		indexValue = indexValue + MBR[j]
	return indexValue

#priority queue class to implement priority queue. Here heapq library is used to implement priority queue
class PriorityQueue:
	def __init__(self):
		self._queue = []
		self._index = 0

	def push(self, item, priority):
		heapq.heappush(self._queue, (priority, self._index, item))
		self._index += 1

	def pop(self):
		return heapq.heappop(self._queue)[-1]

	def empty(self):
		return len(self._queue)


class Node(object):
	"""docstring for node"""
	def __init__(self, MBR = [] , level = 0, index = None, parent = None):
		self.MBR = MBR
		self.level = level
		self.index = index
		self.parent = parent


class RTree(object):
	"""docstring for RTree"""
	def __init__(self, leaves = None, MBR = [], level = 1, minEle = 4, maxEle = 8, parent = None):
		self.MBR = MBR
		self.minEle = minEle
		self.maxEle = maxEle
		self.level = level
		self.parent = parent
		self.leaves = []

	#fid the leaf node
	def findLeafNode(self, Node):
		res = []

		if self.level == 1 : 
			for leaf in self.leaves:
				if leaf.index == Node.index :
					return self
		else :
			for leaf in self.leaves:
				if contain(leaf.MBR, Node.MBR):
					res.append(leaf.findLeafNode(Node))
			for val in res:
				if val != None :
					return val

	#start skyline algorithm
	def findSkylinesStart(self, dims):
		queue = PriorityQueue()
		global comparisons
		skyline = []
		for leaf in self.leaves:
			queue.push(leaf,indexingValue(leaf.MBR, dims))

		while queue.empty() != 0:
			obj = queue.pop()
			if notDominated(skyline, obj.MBR, dims) :
				if obj.level > 0 :
					for leaf in obj.leaves:
						if notDominated(skyline, leaf.MBR, dims):
							queue.push(leaf,indexingValue(leaf.MBR, dims))
				else :
					skyline.append((obj.index, obj.MBR))
		return skyline, comparisons  

	#select leaf node
	def selectLeaf(self, Node):
		#if already a leaf node
		if self.level == Node.level + 1 :
			return self
		else :
			minIncreaseInVolume = 100000000
			minIncreaseInVolumeIdx = -1
			for i in range(0, len(self.leaves)):
				increaseInVolume = increaseVolume(self.leaves[i].MBR, Node.MBR)
				if increaseInVolume < minIncreaseInVolume :
					minIncreaseInVolume = increaseInVolume
					minIncreaseInVolumeIdx = i
			return self.leaves[minIncreaseInVolumeIdx].selectLeaf(Node)


	def splitNode(self):
		#if parent is not present
		if self.parent == None :
			self.parent = RTree(level = self.level + 1, minEle = self.minEle, maxEle = self.maxEle)
			self.parent.leaves.append(self)

		leafa = RTree(level = self.level, minEle = self.minEle, maxEle = self.maxEle, parent = self.parent)
		leafb = RTree(level = self.level, minEle = self.minEle, maxEle = self.maxEle, parent = self.parent)
		#Pick first entry for each group 
		self.linearpickseeds(leafa, leafb)
		while len(self.leaves) > 0:
			#If one group has so few entries that all the rest must be assigned to it m order for it to have the muumum number m, assign them and stop 
			if len(leafa.leaves) > len(leafb.leaves) and len(leafb.leaves) + len(self.leaves) == self.minEle:
				for leaf in self.leaves:
					leafb.MBR = merge(leafb.MBR, leaf.MBR)
					leafb.leaves.append(leaf)
					leaf.parent = leafb
				self.leaves = []
				##If all entnes have been assigned, stop 
				break
			if len(leafb.leaves) > len(leafa.leaves) and len(leafa.leaves) + len(self.leaves) == self.minEle:
				for leaf in self.leaves:
					leafa.MBR = merge(leafa.MBR, leaf.MBR)
					leafa.leaves.append(leaf)
					leaf.parent = leafa
				self.leaves = []
				#If all entnes have been assigned, stop 
				break
			# Invoke Algorithm PickNext to choose the next entry to assign 
			self.pickNext(leafa, leafb)

		self.parent.leaves.remove(self)
		self.parent.leaves.append(leafa)
		self.parent.leaves.append(leafb)
		self.parent.MBR = merge(self.parent.MBR, leafa.MBR)
		self.parent.MBR = merge(self.parent.MBR, leafb.MBR)

	#linear pick seeds algorithm
	def linearpickseeds(self, leaf1, leaf2):
		dimension = len(self.MBR)/2
		wid_d = 0
		temp_wid_d = 0
		wid_i = -1
		wid_j = -1

		lower_max = 0
		lower_max_index = 0
		upper_min = 10000000
		upper_min_index = 0
		for index in range(0, dimension):
			for i in range(0, len(self.leaves)):
				if self.leaves[i].MBR[index] > lower_max :
					lower_max = self.leaves[i].MBR[index]
					lower_max_index = i
			for i in range(0, len(self.leaves)):
				if self.leaves[i].MBR[index+dimension] < upper_min :
					if not i == lower_max_index :
						upper_min = self.leaves[i].MBR[index+dimension]
						upper_min_index = i
			temp_wid_d = abs(self.leaves[upper_min_index].MBR[index+dimension] - self.leaves[lower_max_index].MBR[index])
			temp_wid_d = temp_wid_d/(self.MBR[index+dimension] - self.MBR[index])
			if temp_wid_d > wid_d :
				wid_d = temp_wid_d
				wid_i = min(upper_min_index, lower_max_index)
				wid_j = max(lower_max_index, upper_min_index)

		n2 = self.leaves.pop(wid_j)
		n2.parent = leaf1
		leaf1.leaves.append(n2)
		leaf1.MBR = leaf1.leaves[0].MBR
		n1 = self.leaves.pop(wid_i)
		n1.parent = leaf2
		leaf2.leaves.append(n1)
		leaf2.MBR = leaf2.leaves[0].MBR

	#it will pick next leaf from the pool of leaves
	def pickNext(self, leaf1, leaf2):
		d = 0
		t = 0
		
		for i in range(0,len(self.leaves)):
			#For each entry E not yet m a group, calculate d,= the area increase required in the covermg rectangle of Group 1 to include EI Calculate d2 similarly for Group 2 
			d1 = increaseVolume(merge(leaf1.MBR, self.leaves[i].MBR), leaf1.MBR)
			d2 = increaseVolume(merge(leaf2.MBR, self.leaves[i].MBR), leaf2.MBR)
			#Choose any entry with the maximum difference between d1 and d2
			if abs(d1 - d2) > abs(d):
				d = d1 - d2
				t = i
		# if d > 0  it means d1 > d2 so choosing leaf2
		if d > 0:
			target = self.leaves.pop(t)
			leaf2.MBR = merge(leaf2.MBR, target.MBR)
			target.parent = leaf2
			leaf2.leaves.append(target)
		else:
			target = self.leaves.pop(t)
			leaf1.MBR = merge(leaf1.MBR, target.MBR)
			target.parent = leaf1
			leaf1.leaves.append(target)


	#adjust the tree i.e. if number of nodes is more than maximum allowed value then it splits that node.
	def AdjustTree(self):
		p = self
		#If N is the root, stop 
		while p != None:
			if len(p.leaves) > p.maxEle:
				p.splitNode()
			else:
				if p.parent != None:
					#Adjust covering rectangle in parent entry
					p.parent.MBR = merge(p.parent.MBR, p.MBR)
			p = p.parent

def getBlockParametersDimension(queryfile, dims, blocksize):
	query = open(queryfile, 'r')
	line1 = query.readline().rstrip()
	dims = line1.split('\t')
	dims = map(int, dims)
	line2 = query.readline().rstrip()
	diskpagesize = int(line2)
	line3 = query.readline().rstrip()
	line3 = line3.split('\t')
	pointer_size = int(line3[0])
	key_size = int(line3[1])
	query.close()
	blocksize = int(math.floor(diskpagesize/(pointer_size+key_size)))
	return dims, blocksize

if __name__ == '__main__':
	startTime = time.time()
	data = {}
	#get dimension on which skylines are to be found and memory blocksize 	
	queryfile = 'sample_query.txt'
	dims = []
	blocksize  = 2
	dims, blocksize = getBlockParametersDimension(queryfile, dims, blocksize)
	root = RTree(minEle = blocksize/2, maxEle = blocksize)

	#get input file of objects
	infilename = 'sample_ant.txt'
	outfilename = 'output_ant1.txt'
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
		n.append(Node(MBR = data, index = index))
	inputfile.close()

	for i in range(0, len(n)):
		root = insert(root, n[i])

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

#   Reference:: http://www-db.deis.unibo.it/courses/SI-LS/papers/Gut84.pdf to implement rtree