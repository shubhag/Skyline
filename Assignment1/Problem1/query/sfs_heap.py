import math
import os
import bisect
import os
import time
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

#mergesort files passed in argument as startindex and lastindex of file using heap
def mergePass(startpass, endpass, end):
	size = endpass - startpass + 1
	filenames = list()
	#creates a list that contains the names of the file that we have to merge
	for index in range(startpass, endpass+1):
		fname = 'temp'+str(index)+'.txt'
		filenames.append(fname)
	
	#opens all the files that we have to mergesort
	listLength = len(filenames)
	file_in = [None] * listLength
	i = 0
	for item in filenames:
		file_in[i] = open(item, 'r')
		i += 1
	
	end = end + 1
	#opens the file to which we output the mergesort result
	outfilename = 'temp'+str(end) + '.txt'
	outfile = open(outfilename, 'w')

	heap = []
	#inserts first elements of files in the heap then we use extract min to get minkey
	for i in range(0, listLength):
		readL = file_in[i].readline()
		readL = readL.rstrip().lstrip()
		obj = readL.split('\t')
		insertKey(heap, float(obj[0]) , obj, i)

	#loop it till mergesort is not complete
	while len(heap) > 0:
		minimum = extractMin(heap)
		printListToFile(outfile, minimum.obj)
		#get the fileindex of minimum element. if that file is not empty, insert element in heap from that file
		index = minimum.fromIndex
		readL = file_in[index].readline()
		#inserting from minimum element indexfile if that file is not empty o/w insert from any file which is not empty 
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
	#close all file and delete the unnecessary temporary files
	for item in filenames:
		file_in[i].close()
		os.remove(filenames[i])
		i += 1

	outfile.close()
	#return output file index
	return end

#opens blocksize or less number of sorted tempfiles and call mergePass to mergesort them using heap
def mergeSortedFile(start, end, blocksize):
	while start != end:
		startpass = start
		if end < startpass + blocksize - 1:
			endpass = end
		else:
			endpass = startpass + blocksize -1

		#mergesort function
		end = mergePass(startpass, endpass, end)
		start = endpass + 1
	return end

def readFromInputAndMege(inputfile, dims, blocksize):
	indata = open(inputfile, 'r')
	i = 0
	j = 0
	tupleArray = []

	# it will take blocksize elements from memory, sort it and output them to temporary file
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
	# at the end, i=0 if last tempfile is of size blocksize else last tempfile size is less than blocksize then it is not detected in while loop so checking it here 
	if i > 0 :
		sorted(tupleArray,key=lambda x: x[0])
		filename = 'temp'+str(j) +'.txt'
		printTupleToFile(filename, tupleArray)
		j += 1
	indata.close()

	#mergesort the tempfiles 
	return mergeSortedFile(0, j-1, blocksize)

comparisons = 0
id_list = []
#reports dominance of obj1 over obj2 in dims
def dominating(obj1, obj2, dims):
	flag = False
	for index in dims:
		if obj1[index] < obj2[index]:
			flag = True
		elif obj1[index] > obj2[index]:
			return False
	return flag

#check if an object dominates any other object in memory or not  
#return 1 if newObj dominates some obj in memory, -1 if dominated by some object and 0 if not dominated by anyone(this can still be skyline)
def dominatingInMemory(memoryObj, newObj, timestamp, dims, blocksize):
	global comparisons
	#iterating in a copy of memoryObj so that delete can be done
	for item in memoryObj[:]:
		comparisons += 1
		memObj = item[1]
		#true if newObj dominates memoryObj in dims
		if dominating(newObj, memObj, dims):		
			memoryObj.remove(item)
		elif dominating(memObj, newObj, dims):
			return -1
	if len(memoryObj) < blocksize:
		bisect.insort(memoryObj, (timestamp, newObj))
		return 1
	else:
		return 0

def writeTupleToFile(tempfile, obj):
	tempfile.write(str(obj[0]))
	tempfile.write('\t')
	for y in obj[1]:
		tempfile.write(str(y))
		tempfile.write('\t')
	tempfile.write('\n')

def writeObjectOutput(tempfile, obj):
	for item in obj:
		tempfile.write(str(item))
		tempfile.write('\t')
	tempfile.write('\n')

def outputObjBeforeTimestamp(memoryObj, timestamp):
	global id_list
	copy = memoryObj
	for item in copy:
		if timestamp > item[0]:
			id_list.append(item[1][0])
			memoryObj.remove(item)
		else:
			break

	return memoryObj
def flushMemoryToOutput(memoryObj):
	global id_list
	for obj in memoryObj:
		id_list.append(obj[1][0])

def bnl(infilename, dims, blocksize):
	tempcount = 0
	inputfile = open(infilename, 'r')
	tempfile = open('temp'+str(tempcount)+'.txt', 'w')
	#apply first pass, only blocksize will remain in memory. if others can be skyline they will be placed in tempfile
	timestamp = 1
	elementsInTempfile = 0
	memoryObj = []
	for line in inputfile:
		line = line.rstrip().lstrip()
		obj = line.split('\t')
		#converts string list to int list
		obj = map(float, obj)		
		#return 1 if it dominates some obj in memory, -1 if dominated by some object and 0 if not dominated by anyone(this can still be skyline)
		flag = dominatingInMemory(memoryObj, obj, timestamp, dims, blocksize)
		if flag == 0:
			elementsInTempfile += 1
			writeTupleToFile(tempfile, (timestamp, obj))
		timestamp += 1
	inputfile.close()
	tempfile.close()

	while elementsInTempfile > 0:
		# print elementsInTempfile
		preelementsInTempfile = elementsInTempfile
		elementsInTempfile = 0
		tempcount += 1
		inputfile = open('temp'+str(tempcount-1)+'.txt', 'r')
		tempfile = open('temp'+str(tempcount)+'.txt', 'w')
		for line in inputfile:
			line = line.rstrip()
			arr = line.split('\t')
			# arr = map(int, arr)
			obj = arr[1:] 
			obj = map(float, obj)
			memoryObj = outputObjBeforeTimestamp(memoryObj, int (arr[0]))
			timestamp += 1
			flag = dominatingInMemory(memoryObj, obj, timestamp, dims, blocksize)
			if flag == 0:
				elementsInTempfile += 1
				writeTupleToFile(tempfile, (timestamp, obj))
		inputfile.close()
		tempfile.close()


		os.remove('temp'+str(tempcount-1)+'.txt')
	os.remove('temp'+str(tempcount)+'.txt')
	flushMemoryToOutput(memoryObj)

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
	start_time = time.time()
	dims = []
	blocksize  = 0
	queryfile = 'genfile1.txt'
	#get dimension on which skylines are to be found and memory blocksize 	
	dims, blocksize = getBlockParametersDimension(queryfile, dims, blocksize)

	inputfile = 'genfile2.txt'
	#read input file, sort and merge it using external mergesort(using heap)
	outputfileindex = readFromInputAndMege(inputfile, dims, blocksize)
	print outputfileindex

	infilename = 'gen_inputfile.txt'
	rfile = open('temp'+str(outputfileindex)+'.txt' , 'r')
	wfile = open(infilename, 'w')

	for item in rfile:
		item = item.rstrip().lstrip()
		obj = item.split('\t')
		obj = obj[1:] 
		for i in obj:
			wfile.write(i +'\t')
		wfile.write('\n')

	outfilename = 'output.txt'
	bnl(infilename, dims, blocksize)
	end_time = time.time()

	#print results
	outfile = open(outfilename, 'w')
	outfile.write("Total running time: "+ str(end_time - start_time) + " sec\n")
	outfile.write("Comparisons: "+ str(comparisons)+"\n")
	outfile.write("Size of skyline set: "+str(len(id_list)) + "\n")
	outfile.write("Ids of the skyline objects: \n")

	id_list = map(int, id_list)
	outfile.write(str(id_list))
	outfile.write("\n")
	outfile.close()