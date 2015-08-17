import random
if __name__ == '__main__':
	genfile = open('genfile2.txt', 'w')
	for i in range(1, 1001):
		array = [i]
		for j in range(0,10):
			array.append(random.randint(1,1000))
		for item in array:
			genfile.write(str(item))
			genfile.write('\t')
		genfile.write('\n')
	genfile.close()