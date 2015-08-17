import bisect

main_memory = 40
temp_count = 0
entries_temp = 0

def output_object_before_new(outfile, memory_obj, new_obj, timestamp):
	for tuples in memory_obj:
		if timestamp > tuples[0]:
			write_to_file_wo_time(outfile, tuples[1])
			memory_obj.remove(tuples)
		else:
			return

def nondominating_memory(memory_obj, new_obj, timestamp):
	for tuples in memory_obj:
		obj = tuples[1]
		if dominating(new_obj, obj) :
			memory_obj.remove(tuples)
		elif dominating(obj, new_obj):
			return -1
	global main_memory
	if len(memory_obj) < main_memory:
		bisect.insort(memory_obj, (timestamp, new_obj))
		return 1
	else:
		return 0

def dominating(x, y):
	length = len(x)
	i = 0
	flag = False
	while i < length:
		if(x[i] < y[i]):
			flag = True
		elif(x[i] > y[i]):
			return False
		i = i +1
	if(flag):
		return True
	else:
		return False

def write_to_file_wo_time(tempfile, obj):
	for y in obj:
		tempfile.write(str(y))
		tempfile.write('\t')
	tempfile.write('\n')
	
def write_to_file(tempfile, obj):
	tempfile.write(str(obj[0]))
	tempfile.write('\t')
	for y in obj[1]:
		tempfile.write(str(y))
		tempfile.write('\t')
	tempfile.write('\n')

def flush_memory_output(outputfile, memory_obj):
	for obj in memory_obj:
		# outputfile.write(str(obj[0]))
		# outputfile.write('\t')
		for y in obj[1]:
			outputfile.write(str(y))
			outputfile.write('\t')
		outputfile.write('\n')

if __name__ == '__main__':
	inputfile = open('input.txt', 'r')
	tempfile = open('temp0.txt', 'w')
	outfile = open('outfile.txt', 'w')
	i = 1
	memory_obj = []
	for line in inputfile:
		line = line.lstrip().rstrip()
		obj = line.split('\t')			#obj is an array of string
		obj = map(int, obj)
		flag = nondominating_memory(memory_obj, obj, i)
		if flag == 0:
			entries_temp += 1
			write_to_file(tempfile, (i,obj) )
		i += 1
	inputfile.close()
	tempfile.close()
	# flush_memory_output(outfile, memory_obj)
	# outfile.close()

	while entries_temp > 0 :
		entries_temp = 0
		temp_count += 1
		inputfile = open('temp'+str(temp_count-1)+'.txt', 'r')
		tempfile = open('temp'+str(temp_count)+'.txt', 'w')

		first_time = True
		for line in inputfile:
			arr = line.split('\t')
			if(arr[-1] == "\n"):
				arr.pop(-1)
			arr = map(int, arr)
			obj = arr[1:]
			timestamp = arr[0]
			# print timestamp 
			# print obj
			if first_time:
				output_object_before_new(outfile, memory_obj, obj, timestamp)
				first_time = False
			flag = nondominating_memory(memory_obj, obj, timestamp)
			if flag == 0:
				entries_temp += 1
				write_to_file(tempfile, (timestamp,obj) )
		inputfile.close()
		tempfile.close()

	flush_memory_output(outfile, memory_obj)
	outfile.close()