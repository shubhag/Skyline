import math
import os
from operator import itemgetter


#############################  HEAP IMPLEMENTATION  ####################################################
class Heapobject(object):
	def __init__(self, key, obj, fromIndex):
		super(Heapobject, self).__init__()
		self.key = key
		self.obj = obj
		self.fromIndex = fromIndex

def parent(index):
	return (index-1)/2

def left(index):
	return 2*index + 1

def right(index):
	return 2*index + 2

def insertKey(heap, key, obj, fromIndex):
	heap.append(Heapobject(key, obj, fromIndex))
	i = len(heap) - 1
	while i > 0 and heap[parent(i)].key > heap[i].key:
		heap[parent(i)] , heap[i] = heap[i] , heap[parent(i)]
		i = parent(i)
	return heap

def minHeapify(heap, i):
	l = left(i)
	r = right(i)
	heapsize = len(heap)
	if l < heapsize and heap[l].key < heap[i].key :
		largest = l
	else:
		largest = i
	if r < heapsize and heap[r].key < heap[largest].key :
		largest = r

	if largest != i :
		heap[i], heap[largest] = heap[largest], heap[i]
		minHeapify(heap, largest)

def extractMin(heap):
	heapsize = len(heap)
	if heapsize < 1:
		return -1
	minimum = heap[0]
	heap[0] = heap[heapsize - 1 ] 
	del heap[-1]

	minHeapify(heap, 0)
	return minimum

################# HEAP IMPLEMENTATION END #######################################


def getBlockParametersDimension(queryfile, dims, blocksize):
	query = open(queryfile, 'r')
	line1 = query.readline().rstrip()
	dims = line1.split('\t')
	dims = map(int, dims)
	line2 = query.readline().rstrip()
	blocksize = int (line2)
	query.close()
	return dims, blocksize

def getEntropy(obj, dims):
	entropy = 0 
	for index in dims:
		entropy += math.log(int(obj[index]) + 1 )
	return entropy

def printTupleToFile(filename, tupleArray):
	outTempfile = open(filename, 'w')
	for obj in tupleArray:
		outTempfile.write(str(obj[0]))
		outTempfile.write('\t')
		for t in obj[1]:
			outTempfile.write(str(t))
			outTempfile.write('\t')
		outTempfile.write('\n')
	outTempfile.close()

def printListToFile(outfile, obj):
	for item in obj:
		outfile.write(str(item))
		outfile.write('\t')
	outfile.write('\n')

def mergePass(startpass, endpass, end):
	size = endpass - startpass + 1
	filenames = list()
	for index in range(startpass, endpass+1):
		fname = 'temp'+str(index)+'.txt'
		filenames.append(fname)
	
	listLength = len(filenames)
	file_in = [None] * listLength
	i = 0
	for item in filenames:
		file_in[i] = open(item, 'r')
		i += 1
	
	end = end + 1
	outfilename = 'temp'+str(end) + '.txt'
	outfile = open(outfilename, 'w')

	heap = []
	for i in range(0, listLength):
		readL = file_in[i].readline()
		readL = readL.rstrip().lstrip()
		obj = readL.split('\t')
		insertKey(heap, float(obj[0]) , obj, i)

	file_empty = [False] * listLength
	while len(heap) > 0:
		minimum = extractMin(heap)
		printListToFile(outfile, minimum.obj)
		index = minimum.fromIndex
		readL = file_in[index].readline()
		if readL:
			readL = readL.rstrip().lstrip()
			obj = readL.split('\t')
			insertKey(heap, float(obj[0]) , obj, index)
		else:
			for i in range(0, listLength):
				readL = file_in[i].readline()
				if readL:
					readL = readL.rstrip().lstrip()
					obj = readL.split('\t')
					insertKey(heap, float(obj[0]) , obj, i)
					break

	i = 0
	for item in filenames:
		file_in[i].close()
		os.remove(filenames[i])
		i += 1

	outfile.close()
	return end

def mergeSortedFile(start, end, blocksize):
	while start != end:
		startpass = start
		if end < startpass + blocksize - 1:
			endpass = end
		else:
			endpass = startpass + blocksize -1

		end = mergePass(startpass, endpass, end)
		start = endpass + 1
	return end

def readFromInputAndMege(inputfile, dims, blocksize):
	indata = open(inputfile, 'r')
	i = 0
	j = 0
	tupleArray = []
	for line in indata:
		line = line.rstrip().lstrip()
		obj = line.split('\t')
		entropy = getEntropy(obj, dims)
		objTuple = [entropy, obj]
		tupleArray.append(objTuple)
		i = i + 1
		if i == blocksize:
			tupleArray = sorted(tupleArray,key=itemgetter(0))
			filename = 'temp'+str(j) +'.txt'
			printTupleToFile(filename, tupleArray)
			tupleArray = []
			j += 1
			i = 0

	if i > 0 :
		sorted(tupleArray,key=lambda x: x[0])
		filename = 'temp'+str(j) +'.txt'
		printTupleToFile(filename, tupleArray)
		j += 1
	indata.close()

	return mergeSortedFile(0, j-1, blocksize)
if __name__ == '__main__':
	dims = []
	blocksize  = 0
	queryfile = 'genfile1.txt'
	dims, blocksize = getBlockParametersDimension(queryfile, dims, blocksize)

	inputfile = 'genfile2.txt'
	outputfileindex = readFromInputAndMege(inputfile, dims, blocksize)
	print outputfileindex
	# outputfile = readFromInputAndMege(inputfile, dims, blocksize)