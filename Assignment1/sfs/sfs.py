import math
from operator import itemgetter
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

def printToFile(filename, tupleArray):
	outTempfile = open(filename, 'w')
	for obj in tupleArray:
		outTempfile.write(str(obj[0]))
		outTempfile.write('\t')
		for t in obj[1]:
			outTempfile.write(str(t))
			outTempfile.write('\t')
		outTempfile.write('\n')
	outTempfile.close()

def mergePass(startpass, endpass, end):
	size = endpass - startpass + 1
	filenames = list()
	for index in range(startpass, endpass+1):
		fname = 'temp'+str(index)+'.txt'
		filenames.append(fname)
	file_in = [None] * len(filenames)
	i = 0
	
	for item in filenames:
		file_in[i] = open(item, 'r')
		i += 1

	

	i = 0
	for item in filenames:
		file_in[i].close()
		i += 1

def mergeSortedFile(start, end, blocksize):
	startpass = start
	if end < startpass + blocksize - 1:
		endpass = end
	else:
		endpass = startpass + blocksize -1

	end = mergePass(startpass, endpass, end)
	start = endpass + 1


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
			printToFile(filename, tupleArray)
			tupleArray = []
			j += 1
			i = 0

	if i > 0 :
		sorted(tupleArray,key=lambda x: x[0])
		filename = 'temp'+str(j) +'.txt'
		printToFile(filename, tupleArray)
		j += 1
	indata.close()

	mergeSortedFile(0, j-1, blocksize)
if __name__ == '__main__':
	dims = []
	blocksize  = 0
	queryfile = 'query1.txt'
	dims, blocksize = getBlockParametersDimension(queryfile, dims, blocksize)

	inputfile = 'sample1.txt'
	readFromInputAndMege(inputfile, dims, blocksize)
	# outputfile = readFromInputAndMege(inputfile, dims, blocksize)