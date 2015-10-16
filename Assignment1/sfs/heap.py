class Heapobject(object):
	def __init__(self, key):
		super(Heapobject, self).__init__()
		self.key = key

def parent(index):
	return (index-1)/2

def left(index):
	return 2*index + 1

def right(index):
	return 2*index + 2

def insertKey(heap, key):
	heap.append(Heapobject(key))
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

if __name__ == '__main__':
	heap = []
	insertKey(heap,16)
	insertKey(heap,14)
	insertKey(heap,10)
	insertKey(heap,9)
	insertKey(heap,1)
	insertKey(heap,2)
	insertKey(heap,3)
	print heap
	print extractMin(heap).key
	print extractMin(heap).key
	print extractMin(heap)
	print extractMin(heap)
	print extractMin(heap)
	print extractMin(heap)
	print extractMin(heap)
	print heap