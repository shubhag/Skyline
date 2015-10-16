#include <bits/stdc++.h>
using namespace std;

int heap[1001];
int len = 0 ;
int man = 0 ; 

int parent(int idx){
	return (idx-1)/2;
}

int left(int idx){
	return 2*idx + 1;
}

int right(int idx){
	return 2*idx + 2;
}

void swap(int a, int b){
	int temp = heap[a];
	heap[a] = heap[b];
	heap[b] = temp;

	if(man == a){
		man = b;
	}
	else if(man == b){
		man = a;
	}

}

void insertKey(int key){
	heap[len] = key;
	int i = len;
	len++;
	while( i > 0 && heap[parent(i)] > heap[i]){
		swap(parent(i), i );
		i = parent(i);
	}
}

int minHeapify(int i){
	int l = left(i);
	int r = right(i);
	int largest;
	if (l < len && heap[l] < heap[i]){
		largest = l;
	}else{
		largest = i;
	}
	if(r < len && heap[r] < heap[largest]){
		largest = r;
	}

	if(largest != i){
		swap(i, largest);
		minHeapify(largest);
	}
}

int decreaseKey(){
	heap[0]--;
	minHeapify(0);
}

int increaseKey(){
	heap[man]++;
	int i = man;
	while(i > 0 && heap[parent(i)] < heap[i]){
		swap(parent(i), i);
		i = parent(i);
	}
}

int main(){
	int n, temp, l;
	scanf("%d",&n);
	scanf("%d",&temp);
	l = temp;
	insertKey(temp);
	for (int i = 1; i < n; ++i)
	{
		scanf("%d",&temp);
		if(temp >= l) insertKey(temp);
	}
	int count = 0;
	while(man != 0){
		decreaseKey();
		increaseKey();
		count++;
	}
	if(len > 2 && (heap[0] == heap[1] || heap[0] == heap[2]))
	{
		count++;
	}
	else if(len > 1 && heap[0] == heap[1]  ){
		count++;
	}
	cout << len << endl;
}