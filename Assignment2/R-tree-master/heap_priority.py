import heapq

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)

    def empty(self):
    	return len(self._queue)

q = PriorityQueue()
q.push("faff", 19)
q.push("saff", 9)
q.push("qaff", 119)
q.push("waff", 0)
q.push("eaff", 1)
print q.pop()
print q.pop()
print q.pop()
print q.pop()
print q.pop()
print q.empty()
