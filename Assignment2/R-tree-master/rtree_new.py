#!/usr/bin/python
# -*- coding: utf-8 -*-
import heapq
comparisons = 0
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

class node(object):
	def __init__(self, MBR = None, level = 0, index = None, father = None):
		if(MBR == None):
			self.MBR = []
		else:
			self.MBR = MBR
		self.level = level
		self.index = index
		self.father = father

class Rtree(object):
	def __init__(self, leaves = None, MBR = None, level = 1, m = 1, M = 3, father = None):
		self.leaves = []
		if(MBR == None):
			self.MBR = []
		else:
			self.MBR = MBR
		self.level = level 
		self.m = m
		self.M = M
		self.father = father

	def ChooseLeaf(self, node):
		if self.level == node.level + 1:
			return self
		else:
			increment = [(i, space_increase(self.leaves[i].MBR, node.MBR)) for i in range(len(self.leaves))]
			res = min(increment, key = lambda x:x[1])
			return self.leaves[res[0]].ChooseLeaf(node)

	def SplitNode(self):
		if self.father == None:
			self.father = Rtree(level = self.level + 1, m = self.m, M = self.M)
			self.father.leaves.append(self)
		leaf1 = Rtree(level = self.level, m = self.m, M = self.M, father = self.father)
		leaf2 = Rtree(level = self.level, m = self.m, M = self.M, father = self.father)
		
		self.PickSeeds(leaf1, leaf2)
		
		while len(self.leaves) > 0:
			
			if len(leaf1.leaves) > len(leaf2.leaves) and len(leaf2.leaves) + len(self.leaves) == self.m:
				for leaf in self.leaves:
					leaf2.MBR = merge(leaf2.MBR, leaf.MBR)
					leaf2.leaves.append(leaf)
					leaf.father = leaf2
				self.leaves = []
				break
			if len(leaf2.leaves) > len(leaf1.leaves) and len(leaf1.leaves) + len(self.leaves) == self.m:
				for leaf in self.leaves:
					leaf1.MBR = merge(leaf1.MBR, leaf.MBR)
					leaf1.leaves.append(leaf)
					leaf.father = leaf1
				self.leaves = []
				break
			
			self.PickNext(leaf1, leaf2)
		
		self.father.leaves.remove(self)
		self.father.leaves.append(leaf1)
		self.father.leaves.append(leaf2)
		self.father.MBR = merge(self.father.MBR, leaf1.MBR)
		self.father.MBR = merge(self.father.MBR, leaf2.MBR)
		

	def PickSeeds(self, leaf1, leaf2):
		d = 0
		t1 = 0
		t2 = 0
		
		for i in range(len(self.leaves)):
			for j in range(i + 1, len(self.leaves)):
				MBR_new = merge(self.leaves[i].MBR, self.leaves[j].MBR)
				S_new = getSpace(MBR_new)
				S1 = getSpace(self.leaves[i].MBR)
				S2 = getSpace(self.leaves[j].MBR)
				if S_new - S1 - S2 > d:
					t1 = i
					t2 = j
					d = S_new - S1 - S2
		n2 = self.leaves.pop(t2)
		n2.father = leaf1
		leaf1.leaves.append(n2)
		leaf1.MBR = leaf1.leaves[0].MBR
		n1 = self.leaves.pop(t1)
		n1.father = leaf2
		leaf2.leaves.append(n1)
		leaf2.MBR = leaf2.leaves[0].MBR


	def PickNext(self, leaf1, leaf2):
		d = 0
		t = 0
		
		for i in range(len(self.leaves)):
			d1 = space_increase(merge(leaf1.MBR, self.leaves[i].MBR), leaf1.MBR)
			d2 = space_increase(merge(leaf2.MBR, self.leaves[i].MBR), leaf2.MBR)
			if abs(d1 - d2) > abs(d):
				d = d1 - d2
				t = i
		if d > 0:
			target = self.leaves.pop(t)
			leaf2.MBR = merge(leaf2.MBR, target.MBR)
			target.father = leaf2
			leaf2.leaves.append(target)
		else:
			target = self.leaves.pop(t)
			leaf1.MBR = merge(leaf1.MBR, target.MBR)
			target.father = leaf1
			leaf1.leaves.append(target)


	def AdjustTree(self):
		p = self
		while p != None:
			
			if len(p.leaves) > p.M:
				p.SplitNode()
			else:
				if p.father != None:
					p.father.MBR = merge(p.father.MBR, p.MBR)
			p = p.father


	def Search(self, MBR):
		result = []
		
		if self.level == 1:
			for leaf in self.leaves:
				if intersect(MBR, leaf.MBR):
					result.append(leaf.index)
			return result
		
		else:
			for leaf in self.leaves:
				if intersect(MBR, leaf.MBR):
					result = result + leaf.Search(MBR)
			return result


	def FindLeaf(self, node):
		result = []
		if self.level != 1:
			for leaf in self.leaves:
				if contain(leaf.MBR, node.MBR):
					result.append(leaf.FindLeaf(node))
			for x in result:
				if x != None:
					return x
		else:
			for leaf in self.leaves:
				if leaf.index == node.index:
					return self


	def findSkylinesStart(self, dims):
		queue = PriorityQueue()
		global comparisons
		skyline = []
		for leaf in self.leaves:
			queue.push(leaf,indexingValue(leaf.MBR))

		while queue.empty() != 0:
			obj = queue.pop()
			if notDominated(skyline, obj.MBR, dims) :
				if obj.level > 0 :
					for leaf in obj.leaves:
						queue.push(leaf,indexingValue(leaf.MBR))
				else :
					skyline.append((obj.index, obj.MBR))
		return skyline, comparisons             

def indexingValue(MBR):
	d = len(MBR)/2
	indexValue = 0
	for i in range(0, d):
		indexValue = indexValue + MBR[i]
	return indexValue

def Insert(root, node):
	target = root.ChooseLeaf(node)
	node.father = target
	target.leaves.append(node)
	target.MBR = merge(target.MBR, node.MBR)
	target.AdjustTree()
	if root.father != None:
		root = root.father
	return root

def merge(MBR1, MBR2):
	if len(MBR1) == 0 :
		return MBR2
	if len(MBR2) == 0 :
		return MBR1
	MBR = []
	d = len(MBR1)/2 
	for i in range(0, d):
		MBR.append(min(MBR1[i], MBR2[i]))

	for i in range(d, 2*d):
		MBR.append(max(MBR1[i], MBR2[i]))
	return MBR


def space_increase(MBR1, MBR2):
	d = len(MBR1)/2 
	currSpace = 1.0
	for i in range(0,d):
		currSpace = currSpace * (MBR1[i+d] - MBR1[i])

	newSpace = 1.0
	for i in range(0,d):
		newSpace = newSpace * (max(MBR1[i+d], MBR2[i+d]) - min(MBR1[i], MBR2[i]))

	return newSpace - currSpace    

def intersect(MBR1, MBR2):
	d = len(MBR1)/2
	for i in range(0,d):
		if MBR1[i] > MBR2[i+d]:
			return 0

	for i in range(0,d):
		if MBR1[i+d] < MBR2[i]:
			return 0    
	return 1

def contain(MBR1, MBR2):
	d = len(MBR1)/2
	for i in range(0,d):
		if MBR1[i] > MBR2[i]:
			return 0

	for i in range(0,d):
		if MBR1[i+d] < MBR2[i+d]:
			return 0
	return 1

def getSpace(MBR):
	d = len(MBR)/2 
	space = 1.0
	for i in range(0,d):
		space = space * (MBR[i+d] - MBR[i])
	return space

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