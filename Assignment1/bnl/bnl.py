import bisect
import os
import time

comparisons = 0
id_list = []
#reports dominance of obj1 over obj2 in dims
def dominating(obj1, obj2, dims):
	global comparisons
	flag = False
	comparisons += 1
	for index in dims:
		if obj1[index] < obj2[index]:
			flag = True
		elif obj1[index] > obj2[index]:
			return False
	return flag

#check if an object dominates any other object in memory or not  
#return 1 if newObj dominates some obj in memory, -1 if dominated by some object and 0 if not dominated by anyone(this can still be skyline)
def dominatingInMemory(memoryObj, newObj, timestamp, dims, blocksize):
	#iterating in a copy of memoryObj so that delete can be done
	for item in memoryObj[:]:
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
	queryfile = 'sample_query.txt'
	#get dimension on which skylines are to be found and memory blocksize 	
	dims, blocksize = getBlockParametersDimension(queryfile, dims, blocksize)
	infilename = 'sample_cor.txt'
	outfilename = 'output_cor.txt'
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