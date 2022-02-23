from random import randint

class SortArray:

    def __init__(self, size=100):
        self._size = size
        self._data = list(range(1,self._size+1))
        self._swaps = 0;
        self._comps = 0;
        self.reset(self._size)
        
    def shuffleData(self):
        for i in range(self._size):
            r = randint(0,self._size-1)
            self.swap(i,r)

    def miniShuffleData(self):
        for i in range(self._size):
            r = randint(i-3,i+3)
            if r >= 0 and r < self._size:
                self.swap(i,r)

    def reverseData(self):
        self._data = list(range(self._size, 0,-1))

    def getSize(self):
        return self._size

    def swap(self, i, j):
        self._swaps += 1
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def cmp(self, i, j):
        self._comps += 1
        return self._data[i]-self._data[j]

    def reset(self, size=100, method="shuffle"):
        if size != self._size:
            self._size = size
            self._data = list(range(1,self._size+1))

        self.method = method
        if self.method == "shuffle":
            self.shuffleData();
        elif self.method == "miniShuffle":
            self.miniShuffleData()
        elif self.method == "reverse":
            self.reverseData()
        else:
            raise TypeError("no list organisation method: "+self.method)
    
        self._swaps = 0;
        self._comps = 0;

    def getStats(self):
        return (self._swaps, self._comps)

    def printList(self):
        for i in range(self._size):
            print (self._data[i], end=" ")
        print ()

    def printInfo(self):
        print ("Swaps:", self._swaps, "Comps:", self._comps, "Total:", self._swaps+self._comps)
